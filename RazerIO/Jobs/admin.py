from django.contrib import admin
from .models import JobListing, JobApplication, Job_Categories, Experience_Level_Choices, Job_Info

# Register your models here.
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(Job_Categories)
admin.site.register(Experience_Level_Choices)
admin.site.register(Job_Info)