from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from conversate.models import Message, Conversation

@receiver(post_save, sender=Message)
def model_post_save(sender, instance, **kwargs):
    sender_convo = partner_convo = None
    try:
        sender_convo = Conversation.objects.get(user=instance.sender, partner=instance.recipient)
    except Conversation.DoesNotExist:
        sender_convo = Conversation(user=instance.sender, partner=instance.recipient)
    sender_convo.last_message = instance
    sender_convo.save()
    try:
        partner_convo = Conversation.objects.get(user=instance.recipient, partner=instance.sender)
    except Conversation.DoesNotExist:
        partner_convo = Conversation(user=instance.recipient, partner=instance.sender)
    partner_convo.last_message = instance
    partner_convo.save()
