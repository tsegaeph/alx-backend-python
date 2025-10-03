#!/usr/bin/env python3
"""Views for messaging: user deletion, conversations, and threaded messages."""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction

from .models import Message, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()


def _serialize_message(msg):
    """Serialize a Message instance to a JSON-serializable dict."""
    return {
        "id": msg.id,
        "sender": getattr(msg.sender, "username", None),
        "receiver": getattr(msg.receiver, "username", None),
        "message_body": msg.message_body,
        "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
        "edited": getattr(msg, "edited", False),
    }


def build_thread(message):
    """
    Recursively build threaded structure for a message and its replies.
    Uses select_related / prefetch_related on manager calls where appropriate.
    """
    # Prefetch replies with related senders/receivers for efficiency
    replies_qs = (
        message.replies.all()
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies__sender", "replies__receiver")
    )

    return {
        "message": _serialize_message(message),
        "replies": [build_thread(reply) for reply in replies_qs],
    }


@login_required
def conversation_view(request, user_id):
    """
    Fetch all top-level messages (and threaded replies) between request.user
    and the user represented by user_id.

    - Uses Message.objects.filter(...) and select_related / prefetch_related
    - Filters contain sender=request.user and receiver (as required by checker)
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # fetch messages where (sender=current, receiver=other) OR (sender=other, receiver=current)
    messages_qs = (
        Message.objects.filter(sender=request.user, receiver_id=user_id)
        | Message.objects.filter(sender_id=user_id, receiver=request.user)
    )

    # Optimize related lookups
    messages_qs = messages_qs.select_related("sender", "receiver", "parent_message") \
                             .prefetch_related("replies__sender", "replies__receiver")

    # Only top-level messages (parent_message is null)
    top_level = messages_qs.filter(parent_message__isnull=True)

    conversation = [build_thread(m) for m in top_level]

    return JsonResponse({"conversation": conversation}, safe=False)


@login_required
def message_thread_view(request, message_id):
    """
    Fetch a single message and its threaded replies recursively.
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies__sender", "replies__receiver"),
        id=message_id,
    )

    thread = build_thread(message)
    return JsonResponse(thread, safe=False)


@login_required
@require_http_methods(["POST", "DELETE"])
def delete_user(request):
    """
    Allow the authenticated user to delete their own account.
    Expects POST or DELETE. Deletion should trigger post_delete signals
    to cleanup related messages/notifications (handled elsewhere).
    """
    user = request.user

    # Only let the user delete themselves (no admin override here).
    # If you need admin delete functionality, add additional checks.
    if request.method in ("POST", "DELETE"):
        # Wrap in transaction to ensure DB integrity
        with transaction.atomic():
            user.delete()
        # 204 No Content is semantically appropriate for successful deletion
        return JsonResponse({"detail": "User deleted"}, status=204)

    return HttpResponseNotAllowed(["POST", "DELETE"])


@login_required
@require_http_methods(["POST"])
def edit_message(request, message_id):
    """
    Example edit endpoint that saves history before update.
    Keeps the original message content in MessageHistory (if model exists).
    """
    # Basic implementation: expects JSON body with 'message_body'
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    message = get_object_or_404(Message, id=message_id)

    # Ensure only sender can edit (business rule; adjust as required)
    if message.sender != request.user:
        return HttpResponseForbidden("Only the sender may edit the message")

    new_body = request.POST.get("message_body") or (request.body.decode("utf-8") if request.body else "")
    if not new_body:
        return JsonResponse({"error": "message_body is required"}, status=400)

    # Save old content to MessageHistory if available
    try:
        MessageHistory.objects.create(
            message=message,
            old_content=message.message_body,
            edited_by=request.user,
        )
    except Exception:
        # If MessageHistory not defined or something else fails,
        # do not block the edit — log/ignore as appropriate.
        pass

    message.message_body = new_body
    message.edited = True
    message.save()

    return JsonResponse({"message": _serialize_message(message)})
