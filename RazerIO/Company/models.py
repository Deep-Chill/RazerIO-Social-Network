from django.db import models
# Create your models here.
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from allauth.account.models import EmailAddress
import hashlib
from django.core.exceptions import ValidationError

INDUSTRY_CHOICES = (
    ('SOFTWARE', 'Software'),
    ('HARDWARE', 'Hardware'),
    ('E_COMMERCE', 'E-commerce'),
    ('FINTECH', 'Fintech'),
    ('AI_ML', 'Artificial Intelligence & Machine Learning'),
    ('CLOUD_SERVICES', 'Cloud Services'),
    ('DATA_ANALYTICS', 'Data Analytics'),
    ('CYBER_SECURITY', 'Cybersecurity'),
    ('GAMING', 'Gaming'),
    ('IT_SERVICES', 'IT Services'),
    ('TELECOMMUNICATIONS', 'Telecommunications'),
    ('BLOCKCHAIN', 'Blockchain'),
    ('HEALTHTECH', 'Healthtech'),
    ('EDTECH', 'Edtech'),
    ('IOT', 'Internet of Things'),
    ('AR_VR', 'Augmented & Virtual Reality'),
    ('SOCIAL_MEDIA', 'Social Media'),
)


class EmailDomain(models.Model):
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.domain


class Company(models.Model):
    Name = models.CharField(max_length=256)
    About = models.TextField(max_length=10000, default='', blank=True, null=True)
    Industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True, null=True)
    StockTicker = models.CharField(max_length=10, null=True, blank=True)
    Founded = models.DateField(blank=True, null=True)
    Headquarters = models.CharField(max_length=100, blank=True, null=True)
    Website = models.URLField(blank=True)
    Email_Domain = models.ManyToManyField(EmailDomain, blank=True)
    Logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    IsPublic = models.BooleanField(default=False)

    def clean(self):
        if not self.IsPublic and self.StockTicker:
            raise ValidationError("A company cannot have a StockTicker if it is not public.")
        return super(Company, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.Name

class NotablePerson(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256)
    achievements = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notable_people')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name if self.name else str(self.content_object)

class LeadInvestor(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    amount_invested = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    investment_date = models.DateField(blank=True, null=True)


    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    companies = models.ManyToManyField(Company, related_name='lead_investors')

    def __str__(self):
        return self.name if self.name else str(self.content_object)

class FundingRound(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='funding_rounds')
    round_type = models.CharField(max_length=256)
    date = models.DateField()
    amount_raised = models.DecimalField(max_digits=20, decimal_places=2)
    lead_investors = models.ManyToManyField(LeadInvestor, related_name='lead_investments')

    def __str__(self):
        return f"{self.company.Name} - {self.round_type}"

class Valuation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='valuations')
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.company.Name} - {self.value}"



class University(models.Model):
    Name = models.CharField(max_length=256)
    About = models.TextField(max_length=10000, default='', blank=True, null=True)
    Employees = models.ManyToManyField('Users.CustomUser', blank=True)
    Students = models.IntegerField(null=True, blank=True)
    LastEditedBy = models.ForeignKey('Users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='edited_universities')
    Website = models.URLField(blank=True)
    Email_Domain = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f'{self.Name}'

RATING_CHOICES = [(i, i) for i in range(1, 6)]

SECRET_KEY = "1234567890"

class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user_email_domain = models.CharField(max_length=100, blank=True, null=True)
    user_status = models.CharField(max_length=20, choices=[('Current', 'Current'), ('Former', 'Former')])
    overall_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    culture_and_values_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    senior_leadership_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    compensation_and_benefits_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    career_opportunities_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    work_life_balance_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    future_outlook = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)
    def generate_hash(self, email):
        hash_object = hashlib.sha256((email + SECRET_KEY).encode())
        return hash_object.hexdigest()

    def save(self, *args, **kwargs):
        if not self.user_hash and self.user_email_domain:
            self.user_hash = self.generate_hash(self.user_email_domain)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.company.Name}"



def user_has_verified_email(user, company):
    company_email_domains = company.Email_Domain.values_list('domain', flat=True)
    verified_emails = EmailAddress.objects.filter(user=user, verified=True)
    for email in verified_emails:
        if email.email.split("@")[-1] in company_email_domains:
            return True
    return False

def user_has_not_reviewed_company(user, company):
    verified_emails = EmailAddress.objects.filter(user=user, verified=True)
    for email in verified_emails:
        email_hash = CompanyReview().generate_hash(email.email)
        if company.reviews.filter(user_hash=email_hash).exists():
            print(f'User with email {email.email} has already reviewed this company.')
            return False
    print(f'User with emails {", ".join([email.email for email in verified_emails])} has not reviewed this company yet.')
    return True

class CompanyEditHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="edit_history")
    user = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()
