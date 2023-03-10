from django import forms
from .models import Company

class EditCompanyAboutForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['About']
        labels = {
            'About': 'About the company',
        }
        widgets = {
            'About': forms.Textarea(attrs={'rows': 5}),
        }
