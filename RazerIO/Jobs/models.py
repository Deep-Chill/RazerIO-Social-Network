from django.db import models
from django.conf import settings
from Company.models import Company

User = settings.AUTH_USER_MODEL

# Create your models here.

Job_Categories = (('Programming', 'Programming'), ('Administrative',
                                                   'Administrative'),
                  ('Design', 'Design'), ('Sales & Marketing', 'Sales & Marketing'))
Job_Status_Choices = (('Open', 'Open'), ('Closed', 'Closed'), ('Filled', 'Filled'))
Locations = (('Sacramento', 'Sacramento'), ('San Diego', 'San Diego'),
             ('Los Angeles', 'Los Angeles'), ('Remote', 'Remote'))
class JobListing(models.Model):
    Poster = models.ForeignKey(User, on_delete=models.CASCADE)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Job_Title = models.CharField(max_length=50)
    Job_Description = models.TextField(max_length=5000)
    Job_Requirements = models.TextField(max_length=5000)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Category = models.CharField(choices=Job_Categories, max_length=50)
    Job_Status = models.CharField(choices=Job_Status_Choices, max_length=10)
    Location = models.CharField(choices=Locations, max_length=50)
    Date_Posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.Job_Title} at {self.Company}'

class JobApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    resume = models.CharField(max_length=10000)
    cover_letter = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant} applied at {self.job_listing.Company}'
