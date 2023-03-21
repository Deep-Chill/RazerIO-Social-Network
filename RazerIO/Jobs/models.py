from django.db import models
from django.conf import settings
from Company.models import Company
from Country.models import Country, City

User = settings.AUTH_USER_MODEL

# Create your models here.

# Job_Categories = (
# ('Software Engineering', 'Software Engineering'),
# ('Frontend Development', 'Frontend Development'),
# ('Backend Development', 'Backend Development'),
# ('Full Stack Development', 'Full Stack Development'),
# ('Data Science & Analytics', 'Data Science & Analytics'),
# ('Machine Learning & AI', 'Machine Learning & AI'),
# ('Product & Project Management', 'Product & Project Management'),
# ('UI/UX & Graphic Design', 'UI/UX & Graphic Design'),
# ('IT Operations & Network Engineering', 'IT Operations & Network Engineering'),
# ('Infrastructure & Security', 'Infrastructure & Security'),
# ('Site Reliability & DevOps', 'Site Reliability & DevOps'),
# ('Hardware & Embedded Systems', 'Hardware & Embedded Systems'),
# ('Sales & Marketing', 'Sales & Marketing'),
# ('Finance, Accounting, & Operations', 'Finance, Accounting, & Operations'),
# ('Human Resources & Recruiting', 'Human Resources & Recruiting'),
# ('Customer Support & Success', 'Customer Support & Success'),
# ('Other', 'Other')
# )


Job_Status_Choices = (('Open', 'Open'), ('Closed', 'Closed'), ('Filled', 'Filled'))
# Locations = (('Sacramento', 'Sacramento'), ('San Diego', 'San Diego'),
#              ('Los Angeles', 'Los Angeles'), ('Remote', 'Remote'))

# EXPERIENCE_LEVEL_CHOICES = [
# ('Entry', 'Entry'),
# ('Junior', 'Junior'),
# ('Mid-level', 'Mid-level'),
# ('Senior', 'Senior'),
# ('Principal', 'Principal'),
# ]

class Job_Info(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Job_Categories(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Experience_Level_Choices(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class JobListing(models.Model):
    Poster = models.ForeignKey(User, on_delete=models.CASCADE)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Job_Status = models.CharField(choices=Job_Status_Choices, max_length=10)
    Date_Posted = models.DateTimeField(auto_now_add=True)
    Location = models.ManyToManyField(City)
    Experience_Level = models.ManyToManyField(Experience_Level_Choices)
    Category = models.ManyToManyField(Job_Categories)
    ApplicationURL = models.URLField(default='https://www.mycompany.com/applyhere')
    OtherInfo = models.ManyToManyField(Job_Info)

    def __str__(self):
        return f'{self.Company}'

class JobApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        unique_together = ('applicant', 'job_listing')

    def __str__(self):
        return f'{self.applicant} applied at {self.job_listing.Company}'
