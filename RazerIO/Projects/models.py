from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('On Hold', 'On Hold'),
)

LOCATIONS = (
    ('Sacramento', 'Sacramento'),
    ('San Diego', 'San Diego'),
    ('Los Angeles', 'Los Angeles'),
    ('Remote', 'Remote')
)

class Tool(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Experience(models.Model):
    ITEM_TYPES = (
        ('Project', 'Project'),
        ('Certification', 'Certification'),
        ('Publication', 'Publication'),
        ('Award', 'Award'),
        ('Volunteer Work', 'Volunteer Work'),
        ('Other', 'Other'),
    )

    title = models.CharField(max_length=100)
    item_type = models.CharField(choices=ITEM_TYPES, default='Project', max_length=15)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_portfolio_items')
    collaborators = models.ManyToManyField(User, related_name='collaborating_portfolio_items', blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='In Progress', max_length=12)
    looking_for_x_collaborators = models.IntegerField(default=1, blank=True, null=True)
    skills_used = models.ManyToManyField('Users.Skill', related_name='skills_used', blank=True)
    tools_used = models.ManyToManyField(Tool, related_name='tools_used', blank=True)
    location = models.CharField(choices=LOCATIONS, max_length=50, blank=True)
    url = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    project = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.project.title}"


class ProjectComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.project.title}"

