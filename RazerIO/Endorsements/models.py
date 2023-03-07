from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Endorsement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='endorsements_written')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='endorsements_received')
    text = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)
