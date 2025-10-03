#!/usr/bin/env python3
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message_body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # Track edits
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )

    # 🔥 Self-referential FK to support replies (threaded conversations)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    # Recursive method to fetch all replies to this message
    def get_all_replies(self):
        """Recursively fetch all replies for a message in threaded format"""
        replies = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            replies.append({
                "id": reply.id,
                "sender": reply.sender.username,
                "receiver": reply.receiver.username,
                "message_body": reply.message_body,
                "timestamp": reply.timestamp,
                "replies": reply.get_all_replies()
            })
        return replies


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.username} on message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="history_edited"
    )

    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"
