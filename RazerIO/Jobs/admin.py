from django.contrib import admin
from .models import JobListing, JobApplication

# Register your models here.
admin.site.register(JobListing)
admin.site.register(JobApplication)