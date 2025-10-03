#!/usr/bin/env python3
"""Models for messaging app with signals, history, threading, and custom managers."""

from django.db import models
from django.conf import settings
from django.utils import timezone


class MessageHistory(models.Model):
    """Stores previous versions of edited messages."""
    message = models.ForeignKey("Message", on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"History of {self.message.id} edited by {self.edited_by}"


class UnreadMessagesManager(models.Manager):
    """Custom manager to get unread messages for a specific user."""

    def unread_for_user(self, user):
        # Optimized query: filter unread messages for receiver, fetch only needed fields
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "message_body", "timestamp")
        )


class Message(models.Model):
    """Message model with threading, edit tracking, and unread functionality."""

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
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)  # ✅ New field for Task 4

    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # ✅ Custom manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.message_body[:20]}"


class Notification(models.Model):
    """Notification created when a message is sent."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about Message {self.message.id}"
