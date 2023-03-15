from django import forms
from .models import Company, EmailDomain

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

class CreateCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['Name', 'About', 'Industry', 'StockTicker', 'Founded', 'Headquarters', 'LastEditedBy', 'Website']

class EmailDomainForm(forms.ModelForm):
    class Meta:
        model = EmailDomain
        fields = ['domain']