from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL
STATUS_CHOICES = (
    ('IP', 'In Progress'),
    ('C', 'Completed'),
    ('O', 'On Hold'),
)

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='IP', max_length=2)

    def __str__(self):
        return self.title