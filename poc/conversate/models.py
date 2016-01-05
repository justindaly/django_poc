from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class MessageManager(models.Manager):
    def conversations(self, user, partner):
        return Message.objects.filter(
            Q(sender=user) & Q(recipient=partner) | 
            Q(sender=partner) & Q(recipient=user)).order_by('timestamp')

    def conversation(self, user, partner):
        return Message.objects.filter(
            Q(sender=user) & Q(recipient=partner) | 
            Q(sender=partner) & Q(recipient=user)).order_by('-timestamp')

    def conversation_since(self, user, partner, last_id):
        return Message.objects.filter(
            Q(sender=user) & Q(recipient=partner) | 
            Q(sender=partner) & Q(recipient=user)).filter(id__gt=last_id).order_by('timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages')
    recipient = models.ForeignKey(User, related_name='recipients')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(500)])

    objects = MessageManager()

    class meta:
        unqiue_together = ('user', 'recipient', 'timestamp')

class Conversation(models.Model):
    user = models.ForeignKey(User, related_name='conversations')
    partner = models.ForeignKey(User, related_name='partners')
    last_message = models.ForeignKey(Message)

    class meta:
        unqiue_together = ('user', 'partner')
