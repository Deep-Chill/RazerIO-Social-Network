from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Conversation, Participant, Alert
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import SendMessageForm, StartNewConversationForm
from django.db.models import Q
from django.http import HttpResponseForbidden

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

@login_required
def conversation(request, id):
    user = request.user
    conversation = get_object_or_404(Conversation, id=id)
    participants = conversation.participants.all()
    if user not in participants:
        return render(request, 'unauthorized_conversation.html')
    messages = conversation.message_set.order_by('timestamp')
    receiver = Participant.objects.filter(conversation=conversation).first()
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = user
            message.content = form.cleaned_data['content']
            message.receiver = receiver.user
            message.save()
            return redirect('conversation', id=id)
    else:
            form = SendMessageForm(initial={'conversation': conversation})
    context = {
        'conversation':conversation,
        'messages':messages,
        'form':form,
    }
    return render(request, 'conversation.html', context=context)


@login_required
def alerts(request):
    # Get all unread alerts for the current user
    unread_alerts = Alert.objects.filter(recipient=request.user, read=False)

    # Create a copy of the queryset

    # Mark all unread alerts as read

    # Render the alerts template with the new alerts
    return render(request, 'alerts.html', {'alerts': unread_alerts})

def start_new_conversation(request):
    if request.method == "POST":
        form = StartNewConversationForm(request.POST, user=request.user)
        if form.is_valid():
            sender = request.user
            conversation = form.save(commit=True, sender=sender)
            return redirect('conversation', id=conversation.id)
    else:
        form = StartNewConversationForm(user=request.user)
    context = {
        'form':form
    }
    return render(request, 'new_conversation.html', context)