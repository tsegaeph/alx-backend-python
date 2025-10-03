#!/usr/bin/env python3

from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Message, MessageHistory, Notification

User = get_user_model()


@receiver(pre_save, sender=Message)
def log_message_history(sender, instance: Message, **kwargs):
    """
    When an existing Message is updated and the content changed,
    create a MessageHistory entry with the previous content.
    """
    if not instance.pk:  # New message, no history yet
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.message_body != instance.message_body:
        MessageHistory.objects.create(
            message=old,
            old_content=old.message_body,
            edited_at=timezone.now(),
            edited_by=getattr(instance, "edited_by", None),
        )
        if hasattr(instance, "edited"):
            instance.edited = True


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance: Message, created, **kwargs):
    """
    When a new Message is created, generate a Notification for the receiver.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            created_at=timezone.now(),
        )


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance: User, **kwargs):
    """
    When a user is deleted, remove messages, notifications and histories
    related to that user.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
