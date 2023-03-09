from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Conversation, Participant, Message

User = get_user_model()

from django import forms
from .models import Message, Conversation, Participant

class SendMessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), label='Text')
    class Meta:
        model = Message
        fields = ['content']


class StartNewConversationForm(forms.ModelForm):
    subject = forms.CharField(max_length=256, required=False)
    message = forms.CharField(max_length=10000)
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.none())

    class Meta:
        model = Conversation
        fields = ['participants', 'subject']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        recipient = kwargs.pop('recipient', None)
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(
            Q(followers__User=user) & Q(following__Following_User_ID=user)
        ).exclude(id=user.id)

        if recipient:
            self.fields['participants'].initial = [recipient]

    def save(self, commit=True, sender=None):
        conversation = super().save(commit=False)
        if commit:
            conversation.save()
        Participant.objects.create(user=sender, conversation=conversation)
        participants = self.cleaned_data['participants']
        for participant in participants:
            if participant == sender:
                continue
            Participant.objects.create(user=participant, conversation=conversation)
        Message.objects.create(sender=sender, content=self.cleaned_data['message'],
                               conversation=conversation)
        return conversation
