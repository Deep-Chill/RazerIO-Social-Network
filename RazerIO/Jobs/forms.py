from django.forms import Form, ModelForm
from .models import JobListing, JobApplication
from django import forms

class JobPosting(ModelForm):

    class Meta:
        model = JobListing
        fields = ['Company', 'Category', 'Experience_Level', 'Job_Title', 'salary_min', 'salary_max',
                  'MinimumExperience', 'NumberRecruiting', 'ApplicationURL']
    def __init__(self, *args, **kwargs):
        super(JobPosting, self).__init__(*args, **kwargs)
        self.fields['salary_min'].label = "Minimum salary"
        self.fields['salary_max'].label = "Maximum salary"
        self.fields['MinimumExperience'].label = "Years of experience required"
        self.fields['NumberRecruiting'].label = "How many people are being hired for this position?"

class ApplyToJobForm(ModelForm):

    class Meta:
        model = JobApplication
        fields = []
