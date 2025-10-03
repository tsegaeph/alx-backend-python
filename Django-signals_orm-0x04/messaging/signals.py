# messaging/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Deletes all related messages, notifications, and message histories
    when a user is deleted.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to their messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
