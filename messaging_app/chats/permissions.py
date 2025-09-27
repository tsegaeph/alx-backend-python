# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission: Only allow users to access their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # For messages, ensure sender matches the logged-in user
        if hasattr(obj, "sender"):
            return obj.sender == request.user

        # For conversations, ensure the user is part of participants
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False
