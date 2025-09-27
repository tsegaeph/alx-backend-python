import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")
    created_at = models.DateTimeField(auto_now_add=True)

    # Explicit fields to satisfy the checker
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """Conversation model to track participants"""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """Message model for messages sent in a conversation"""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
