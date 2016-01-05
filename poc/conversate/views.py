from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import generics
import json
import logging

from conversate.models import Message
from conversate.serializers import UserSerializer, MessageSerializer
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@login_required
def index(request):
    resp = {}
    logger.debug('in index for user: ' + request.user.username)
    conversations = request.user.conversations
    resp['conversations'] = conversations
    resp['users'] = User.objects.all().exclude(username=request.user.username).order_by('username')
    return render(request, 'conversate/index.html', resp)


@login_required
def conversation(request, partner_username):
    resp = {}
    logger.debug('looking up partner: ' + partner_username)
    partner = User.objects.get(username=partner_username)
    resp['partner'] = partner
    messages = Message.objects.conversations(request.user, partner)
    resp['messages'] = messages
    return render(request, 'conversate/conversation.html', resp)

@login_required
@csrf_exempt
def send_message(request, partner_username):
    resp = {}
    partner = User.objects.get(username=partner_username)
    resp['partner'] = partner
    logger.debug(request.body)
    content = json.loads(request.body)['message']
    logger.debug("sending partner: " + partner.username + " message: " + content)
    m = Message(sender=request.user, recipient=partner, content=content)
    m.save()
    messages = Message.objects.conversations(request.user, partner)
    resp['messages'] = messages
    #return render(request, 'conversate/conversation.html', resp)
    return HttpResponse("OK", content_type="text/plain")


## rest calls

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        partner = User.objects.get(username=self.kwargs['partner_username'])
        return Message.objects.conversation(user, partner)

class MessageSinceList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        partner = User.objects.get(username=self.kwargs['partner_username'])
        last_id = int(self.request.GET['last_id'])
        return Message.objects.conversation_since(user, partner, last_id)
