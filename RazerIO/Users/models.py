from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    Bio = models.CharField(max_length=240, default='')
    Salary = models.IntegerField(default=0)
    Company = models.OneToOneField('Company.Company', on_delete=models.CASCADE,
                                   null=True, blank=True)
    def __str__(self):
        return self.username

class UserFollowing(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    Following_User_ID = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Following_User_ID'], name='unique_followers')
        ]
        ordering = ["-created"]
    def __str__(self):
        return f'{self.User}'
