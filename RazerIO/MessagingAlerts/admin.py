from django.contrib import admin
from .models import Conversation, Message, Participant, Alert

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Participant)
admin.site.register(Alert)