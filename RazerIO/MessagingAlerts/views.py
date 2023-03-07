from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Conversation, Participant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

User = get_user_model()

def inbox(request):
    user = request.user
    participant_conversation_ids = Participant.objects.filter(user=request.user).values_list('conversation', flat=True)
    conversations = Conversation.objects.filter(id__in=participant_conversation_ids)
    context = {'conversations':conversations, 'participantids':participant_conversation_ids}
    return render(request, 'inbox.html', context=context)

def outbox(request):
    user = request.user
    messages = Message.objects.filter(sender=user)
    context = {'messages':messages}
    return render(request, 'outbox.html', context=context)

def conversation(request, id):
    user = request.user
    conversation = Conversation.objects.get(id=id)
    messages = Message.objects.filter(conversation=conversation)
    context = {'conversation':conversation, 'messages':messages}
    return render(request, 'conversation.html', context=context)
