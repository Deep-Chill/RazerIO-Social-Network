from django import forms
from .models import Company, EmailDomain, CompanyReview, NotablePerson, LeadInvestor, Valuation, CompanyEditHistory, NonEmployeeReview
import json
from yahooquery import Ticker
from django.core.exceptions import ValidationError

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

# class CreateCompanyForm(forms.ModelForm):
#
#     class Meta:
#         model = Company
#         fields = ['Name', 'About', 'Industry', 'StockTicker', 'Founded', 'Headquarters', 'Website']

class CreatePublicCompanyForm(forms.ModelForm):
    StockTicker = forms.CharField(required=True)
    class Meta:
        model = Company
        fields = ['Name', 'StockTicker', 'Industry']
        widgets = {
            'StockTicker': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_StockTicker(self):
        stock_ticker = self.cleaned_data['StockTicker']

        # Add your stock ticker validation logic here, e.g., check if it's a valid and not delisted ticker
        is_valid, is_delisted = self.check_stock_ticker(stock_ticker)

        if not is_valid:
            raise ValidationError("The provided stock ticker is not valid.")
        if is_delisted:
            raise ValidationError("The provided stock ticker is for a delisted stock.")

        return stock_ticker

    def check_stock_ticker(self, stock_ticker):
        # Implement your validation logic here, e.g., query an API or database to check the ticker
        ticker = Ticker(stock_ticker)

        try:
            quote_type = ticker.quote_type[stock_ticker]

            if not quote_type:
                return False, False

            if quote_type.get('quoteType') == 'EQUITY' and quote_type.get('exchange') != 'PNK':
                is_delisted = False
            else:
                is_delisted = True

            return True, is_delisted
        except Exception as e:
            print(f"Error fetching data for stock ticker {stock_ticker}: {e}")
            return False, False


class CreatePrivateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Name', 'About', 'Industry', 'Founded', 'Headquarters', 'Website', 'Logo']
        widgets = {
            'StockTicker': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }


class EmailDomainForm(forms.ModelForm):
    domain = forms.CharField(label='Company email domain(after the "@" symbol)', help_text="For example, if a company's email addresses are example@company.com, then you should only write \"company.com\" in the field above.")

    class Meta:
        model = EmailDomain
        fields = ['domain']
        labels = {'domain': 'Company\'s email domain after the @'}

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = [
            'user_status',
            'overall_rating',
            'culture_and_atmosphere_rating',
            'senior_leadership_rating',
            'compensation_and_benefits_rating',
            'career_opportunities_rating',
            'future_outlook',
            'work_life_balance_rating',
            'review_text',
        ]

from django import forms
from .models import Company, NotablePerson, LeadInvestor, Valuation
from django.forms.widgets import ClearableFileInput


class EditCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Industry', 'Founded', 'Headquarters', 'Logo', 'About']
        widgets = {
            'About': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'Founded': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Headquarters': forms.TextInput(attrs={'class': 'form-control'}),
            'Logo': ClearableFileInput(attrs={'class': 'form-control-file'}),
            'Industry': forms.Select(attrs={'class': 'form-control'}),
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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'achievements': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class LeadInvestorForm(forms.ModelForm):
    class Meta:
        model = LeadInvestor
        fields = ['name', 'bio', 'website', 'amount_invested', 'investment_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_invested': forms.NumberInput(attrs={'class': 'form-control'}),
            'investment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class ValuationForm(forms.ModelForm):
    class Meta:
        model = Valuation
        fields = ['date', 'value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class NonEmployeeReviewForm(forms.ModelForm):
    class Meta:
        model = NonEmployeeReview
        fields = [
            'relationship',
            'overall_experience',
            'customer_service_rating',
            'product_quality_rating',
            'review_title',
            'review_text',
            'advice_to_management'
        ]

class ReviewTypeForm(forms.Form):
    REVIEW_TYPE_CHOICES = [
        ('employee', 'I am/was an employee of this company.'),
        ('non_employee', 'I had an experience with this company (customer, vendor, etc.).')
    ]
    review_type = forms.ChoiceField(choices=REVIEW_TYPE_CHOICES, widget=forms.RadioSelect, required=True)
