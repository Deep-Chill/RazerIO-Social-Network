from django.db import models
from django.conf import settings
from django.utils import timezone

Choices = (('National', 'National'), ('Friends', 'Friends'), ('Organization', 'Organization'))

# Create your models here.
class Post(models.Model):
    Author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Date_Created = models.DateTimeField(auto_now_add=True)
    Text = models.TextField(max_length=256, blank=False)
    Category = models.CharField(max_length=15, choices=Choices, default='Friends')

    def __str__(self):
        return f'{self.Author} posted at {self.Date_Created}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def time_elapsed(self):
        delta = timezone.now() - self.Date_Created
        if delta.days > 365:
            return f"{delta.days // 365} years ago"
        if delta.days > 30:
            return f"{delta.days // 30} months ago"
        if delta.days > 0:
            return f"{delta.days} days ago"
        if delta.seconds > 3600:
            return f"{delta.seconds // 3600} hours ago"
        if delta.seconds > 60:
            return f"{delta.seconds // 60} minutes ago"
        return f"{delta.seconds} seconds ago"


class Upvote(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Date_Voted = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    Author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Text = models.TextField(max_length=256, blank=False, null=False)
    Date_Commented = models.DateTimeField(auto_now_add=True)
