from django.db import models
from django.conf import settings

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


class Upvote(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Date_Voted = models.DateTimeField(auto_created=True)

class Comment(models.Model):
    Author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Text = models.TextField(max_length=256, blank=False, null=False)
    Date_Commented = models.DateTimeField(auto_created=True)
