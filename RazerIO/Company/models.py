from django.db import models
# Create your models here.
from django.conf import settings

INDUSTRY_CHOICES = (
    ('SOFTWARE', 'Software'),
    ('HARDWARE', 'Hardware'),
    ('E_COMMERCE', 'E-commerce'),
    ('FINTECH', 'Fintech'),
    ('AI_ML', 'Artificial Intelligence & Machine Learning'),
    ('CLOUD_SERVICES', 'Cloud Services'),
    ('DATA_ANALYTICS', 'Data Analytics'),
    ('CYBER_SECURITY', 'Cybersecurity'),
    ('GAMING', 'Gaming'),
    ('IT_SERVICES', 'IT Services'),
    ('TELECOMMUNICATIONS', 'Telecommunications'),
    ('BLOCKCHAIN', 'Blockchain'),
    ('HEALTHTECH', 'Healthtech'),
    ('EDTECH', 'Edtech'),
    ('IOT', 'Internet of Things'),
    ('AR_VR', 'Augmented & Virtual Reality'),
    ('SOCIAL_MEDIA', 'Social Media'),
)


class EmailDomain(models.Model):
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.domain


class Company(models.Model):
    Name = models.CharField(max_length=256)
    About = models.TextField(max_length=10000, default='', blank=True, null=True)
    Industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True, null=True)
    StockTicker = models.CharField(max_length=10, null=True, blank=True)
    Founded = models.DateField(blank=True, null=True)
    Headquarters = models.CharField(max_length=100, blank=True, null=True)
    LastEditedBy = models.ForeignKey('Users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='edited_companies')
    Website = models.URLField(blank=True)
    Email_Domain = models.ManyToManyField(EmailDomain, blank=True)
    Logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.Name



Anonymous_YN = (('Yes', 'Yes'), ('No', 'No'))

class Company_Review(models.Model):
    Anonymous = models.CharField(choices=Anonymous_YN, blank=False, default='Yes',
                                 max_length=3)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Rating = models.IntegerField()
    Text = models.TextField(max_length=10000)
    Date_Created = models.DateTimeField(auto_created=True)

class University(models.Model):
    Name = models.CharField(max_length=256)
    About = models.TextField(max_length=10000, default='', blank=True, null=True)
    Employees = models.ManyToManyField('Users.CustomUser', blank=True)
    Students = models.IntegerField(null=True, blank=True)
    LastEditedBy = models.ForeignKey('Users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='edited_universities')
    Website = models.URLField(blank=True)
    Email_Domain = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f'{self.Name}'
