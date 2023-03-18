from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from django.core.files import File
from PIL import Image
from Country.models import Country, Region
import uuid
import os
import email_validator
# from allauth.account.models import EmailAddress
from django.forms import ValidationError
from django.dispatch import receiver
# from allauth.account.signals import email_confirmed, email_changed, email_added, email_removed


# Create your models here.

User = settings.AUTH_USER_MODEL

EXPERIENCE_LEVEL_CHOICES = [
('Entry', 'Entry'),
('Junior', 'Junior'),
('Mid-level', 'Mid-level'),
('Senior', 'Senior'),
('Principal', 'Principal'),
]

def upload_to(instance, filename):
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex

    # Get the file extension
    ext = os.path.splitext(filename)[1]

    # Combine the unique identifier and file extension to create the new filename
    new_filename = f"{unique_id}{ext}"

    # Return the new filename
    return os.path.join('profile_pics/', new_filename)

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User_Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience_years = models.IntegerField(default=0)

class CustomUser(AbstractUser):
    Bio = models.CharField(max_length=240, default='')
    Salary = models.IntegerField(default=0)
    Company = models.ForeignKey('Company.Company', on_delete=models.CASCADE,
                                   null=True, blank=True)
    Country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    Region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    ProfilePic = models.ImageField(upload_to=upload_to, null=True, blank=True)
    Skill = models.ManyToManyField(Skill, through="User_Skill")
    Company_Verified_Email = models.BooleanField(default=False)
    badges = models.JSONField(default=dict)
    experience_level = models.CharField(choices=EXPERIENCE_LEVEL_CHOICES, max_length=50, default='Principal')
    DateOfBirth = models.DateField(null=True, blank=True)

    def earn_badge(self, badge_name):
        self.badges[badge_name] = True
        self.save()

    def remove_badge(self, badge_name):
        if not self.badges:
            return False
        try:
            del self.badges[badge_name]
            self.save()
            return True
        except KeyError:
            return False

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



class Education(models.Model):
    DEGREE_TYPE_CHOICES = (
        ('None', 'None'),
        ('High School', 'High School'),
        ('Associate\'s Degree', 'Associate\'s Degree'),
        ('Bachelor\'s Degree', 'Bachelor\'s Degree'),
        ('Master\'s Degree', 'Master\'s Degree'),
        ('Doctorate', 'Doctorate'),
        ('Other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    degree_type = models.CharField(max_length=18, choices=DEGREE_TYPE_CHOICES, default='none')
    major = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, help_text="Describe your thoughts")
    location = models.CharField(max_length=255)
    activities_awards_and_societies = models.TextField(blank=True)
    institution = models.ForeignKey('Company.University', on_delete=models.CASCADE,
                                    default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.degree_type} from {self.institution}"
