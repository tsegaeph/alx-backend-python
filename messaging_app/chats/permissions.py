from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow participants of the conversation
        conversation = getattr(obj, "conversation", None)

        if not conversation:
            return False

        is_participant = (
            request.user == conversation.sender
            or request.user == conversation.receiver
        )

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        return is_participant
