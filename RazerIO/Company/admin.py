from django.contrib import admin
from .models import Company, University, EmailDomain, CompanyReview, NotablePerson, LeadInvestor, Valuation, CompanyEditHistory
# Register your models here.
admin.site.register(Company)
admin.site.register(University)
admin.site.register(EmailDomain)
admin.site.register(CompanyReview)
admin.site.register(NotablePerson)
admin.site.register(LeadInvestor)
admin.site.register(Valuation)
admin.site.register(CompanyEditHistory)