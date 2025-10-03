#!/usr/bin/env python3
"""Models for messaging app (Message, MessageHistory, Notification)."""

from django.db import models
from django.conf import settings
from django.utils import timezone

# import the manager we just created
from .managers import UnreadMessagesManager


class MessageHistory(models.Model):
    """Stores previous versions of edited messages."""
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"History of message {self.message_id} at {self.timestamp}"


class Message(models.Model):
    """Message model with threading, edit tracking, and unread flag."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    message_body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # edited tracking
    edited = models.BooleanField(default=False)
    # who last edited (nullable)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages",
    )

    # Self-referential parent for threaded replies
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    # new field for Task 4
    read = models.BooleanField(default=False)

    # managers
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # checker expects Message.unread.unread_for_user
    unread_messages = UnreadMessagesManager()  # optional alias if you used this before

    def __str__(self):
        return f"Message({self.id}) from {self.sender} to {self.receiver}"


class Notification(models.Model):
    """Notification created when a message is received."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"
