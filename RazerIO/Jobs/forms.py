from django.forms import Form, ModelForm
from .models import JobListing, JobApplication
from django import forms

class JobPosting(ModelForm):

    class Meta:
        model = JobListing
        fields = ['Job_Title', 'Job_Description', 'Company', 'salary_min', 'salary_max', 'Category']

class ApplyToJobForm(ModelForm):
    resume = forms.CharField(label='Resume')
    cover_letter = forms.CharField(label='Cover Letter', widget=forms.Textarea)

    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
