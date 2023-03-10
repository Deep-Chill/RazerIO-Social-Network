from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ('IP', 'In Progress'),
    ('C', 'Completed'),
    ('O', 'On Hold'),
)

LOCATIONS = (
    ('Sacramento', 'Sacramento'),
    ('San Diego', 'San Diego'),
    ('Los Angeles', 'Los Angeles'),
    ('Remote', 'Remote')
)


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='IP', max_length=2)
    looking_for_x_collaborators = models.IntegerField(default=1, blank=True, null=True)
    required_skills = models.ManyToManyField('Users.Skill', related_name='required_for_collaborators', blank=True, max_length=3)
    tech_stack = models.ManyToManyField('Users.Skill', related_name='used_in_project', blank=True)
    location = models.CharField(choices=LOCATIONS, max_length=50, blank=True)
    collaborator_requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.project.title}"


class ProjectComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.project.title}"
