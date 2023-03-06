from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# Create your models here.

# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     text = models.TextField(max_length=10000)
#
