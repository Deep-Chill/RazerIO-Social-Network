from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Message, Conversation, Participant, Alert
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import SendMessageForm, StartNewConversationForm
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def inbox(request, user_id=None):
    user = request.user
    all_alerts = Alert.objects.filter(recipient=user)
    unread_alerts = all_alerts.filter(read=False)
    participant_conversation_ids = Participant.objects.filter(user=request.user).values_list('conversation', flat=True)
    conversations = Conversation.objects.filter(id__in=participant_conversation_ids).order_by('-created_at')
    outmessages = Message.objects.filter(sender=user).select_related('conversation')

    recipient = None
    if user_id:
        recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = StartNewConversationForm(request.POST, user=user)
        if form.is_valid():
            conversation = form.save(sender=user)  # Get the created conversation
            messages.success(request, 'Conversation started successfully.')
            return redirect('conversation', id=conversation.id)  # Use the conversation's ID for redirection
    else:
        form = StartNewConversationForm(user=user, recipient=recipient)
    context = {
        'conversations':conversations,
        'participantids':participant_conversation_ids,
        'form':form,
        'alerts': all_alerts,
        'unread_alerts':unread_alerts,
        'outmessages':outmessages,
        'open_new_message_tab':bool(user_id)
        }
    return render(request, 'inbox.html', context=context)

@login_required
def outbox(request):
    user = request.user
    messages = Message.objects.filter(sender=user).select_related('conversation')
    conversations = Conversation.objects.filter(participants=user).select_related('participants')
    context = {'messages':messages, 'conversations':conversations, }
    return render(request, 'outbox.html', context=context)


@login_required
def conversation(request, id):
    user = request.user
    conversation = get_object_or_404(Conversation, id=id)
    participants = conversation.participants.all()
    if user not in participants:
        return render(request, 'unauthorized_conversation.html')
    messages = conversation.message_set.order_by('timestamp')
    for message in messages:
        if user not in message.read_by.all():
            message.read_by.add(user)
            message.save()
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = user
            message.content = form.cleaned_data['content']
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
def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, recipient=request.user)
    alert.delete()
    messages.success(request, 'Alert deleted successfully.')
    return redirect(reverse('inbox') + '#v-pills-alerts')


@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    user = request.user

    if user in conversation.participants.all():
        participant = get_object_or_404(Participant, user=user, conversation=conversation)
        participant.delete()
        messages.success(request, 'Conversation deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this conversation.')

    return redirect('inbox')
