from django.db import models
from django.conf import settings

# Create your models here.

class Newspaper(models.Model):
    Title = models.CharField(max_length=256)
    Owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='Newspaper')
    Date_Created = models.DateField(auto_created=True)
    Logo = models.ImageField(upload_to='Newspaper/Logos', null=True)

    def __str__(self):
        return f'{self.Title}'

class Article(models.Model):
    Title = models.CharField(max_length=256)
    Date_Published = models.DateTimeField(auto_created=True)
    Text = models.TextField(max_length=16000)
    Newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Title}'

class Article_Comment(models.Model):
    Author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Text = models.TextField(max_length=10000)
    Date_Published = models.DateTimeField(auto_created=True)

# class Article_Votes(models.Model):
#     User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     Article = models.ForeignKey(Article, on_delete=models.CASCADE)
#