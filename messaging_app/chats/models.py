from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email



class Conversation(models.Model):
    """Conversation between multiple users"""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """Message sent by a user in a conversation"""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
