from django.forms import Form, ModelForm, CheckboxSelectMultiple
from .models import JobListing, JobApplication, Job_Categories, Experience_Level_Choices, Job_Info
from django.forms.widgets import SelectMultiple
from Country.models import City
from django import forms
from django.core.exceptions import ValidationError

class JobPosting(ModelForm):
    Category = forms.ModelMultipleChoiceField(queryset=Job_Categories.objects.all(), widget=CheckboxSelectMultiple)
    Location = forms.ModelMultipleChoiceField(queryset=City.objects.all(), widget=SelectMultiple, label='Choose locations:')
    Experience_Level = forms.ModelMultipleChoiceField(queryset=Experience_Level_Choices.objects.all(), widget=CheckboxSelectMultiple)
    OtherInfo = forms.ModelMultipleChoiceField(queryset=Job_Info.objects.all(), widget=CheckboxSelectMultiple)

    class Meta:
        model = JobListing
        fields = ['Company', 'Category', 'Location', 'Experience_Level', 'OtherInfo', 'ApplicationURL']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JobPosting, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get("Company")

        if self.user and company:
            if not self.user.Company_Verified_Email:
                raise ValidationError("Your email address is not verified for the selected company.")

        return cleaned_data


class ApplyToJobForm(ModelForm):

    class Meta:
        model = JobApplication
        fields = []
