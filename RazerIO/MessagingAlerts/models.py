from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# Create your models here.

class Conversation(models.Model):
    participants = models.ManyToManyField(User, through='Participant', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(max_length=256, blank=True, null=True)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

class Alert(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    verb = models.CharField(max_length=255)
    target = models.URLField(null=True, blank=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.recipient.username}: {self.verb}'

    def get_absolute_url(self):
        return reverse('notification_detail', args=[str(self.id)])
