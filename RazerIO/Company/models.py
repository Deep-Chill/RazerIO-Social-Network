from django.db import models
# Create your models here.
from django.conf import settings

class Company(models.Model):
    Name = models.CharField(max_length=256)
    About = models.TextField(max_length=10000, default='', blank=True, null=True)
    Employees = models.ManyToManyField('Users.CustomUser')
    Shareprice = models.IntegerField(default=0, blank=True, null=True)
    StockTicker = models.CharField(max_length=10, null=True, blank=True)
    LastEditedBy = models.ForeignKey('Users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='edited_companies')
    Website = models.URLField(blank=True)
    Email_Domain = models.CharField(blank=True, max_length=50)
    Is_University = models.BooleanField(default=False)

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