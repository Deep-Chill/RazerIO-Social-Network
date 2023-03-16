from django import forms
from .models import Company, EmailDomain, CompanyReview, NotablePerson, LeadInvestor, Valuation, CompanyEditHistory
import json

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
        fields = ['Name', 'About', 'Industry', 'StockTicker', 'Founded', 'Headquarters', 'Website']

class EmailDomainForm(forms.ModelForm):
    class Meta:
        model = EmailDomain
        fields = ['domain']

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = [
            'user_status',
            'overall_rating',
            'culture_and_values_rating',
            'senior_leadership_rating',
            'compensation_and_benefits_rating',
            'career_opportunities_rating',
            'future_outlook',
            'work_life_balance_rating',
            'review_text',
        ]

class EditCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Industry', 'Founded', 'Headquarters', 'Website', 'Logo', 'About']
        widgets = {
            'About': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        company = super(EditCompanyForm, self).save(*args, **kwargs)

        changes = {}
        for field in self.changed_data:
            changes[field] = self.cleaned_data[field]

        serialized_changes = json.dumps(changes)
        edit_history = CompanyEditHistory(company=company, user=user, changes=serialized_changes)
        edit_history.save()

        print("Created CompanyEditHistory object:", edit_history)

        return company


class NotablePersonForm(forms.ModelForm):
    class Meta:
        model = NotablePerson
        fields = ['name', 'title', 'achievements']

class LeadInvestorForm(forms.ModelForm):
    class Meta:
        model = LeadInvestor
        fields = ['name', 'bio', 'website', 'amount_invested', 'investment_date']

class ValuationForm(forms.ModelForm):
    class Meta:
        model = Valuation
        fields = ['date', 'value']
