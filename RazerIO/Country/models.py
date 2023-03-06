from django.db import models

# Create your models here.

class Country(models.Model):
    Name = models.CharField(max_length=56)
    Abbreviation = models.CharField(max_length=5)
    Flag = models.ImageField(upload_to='flags/')
    Currency = models.CharField(max_length=64)
    Currency_Abbreviation = models.CharField(max_length=5)

    def __str__(self):
        return self.Name

class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name