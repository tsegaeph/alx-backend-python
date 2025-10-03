from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    # If it's an existing message (not a new one)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Save old content in history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
