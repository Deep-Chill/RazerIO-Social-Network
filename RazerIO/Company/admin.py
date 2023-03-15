from django.contrib import admin
from .models import Company, University, EmailDomain
# Register your models here.
admin.site.register(Company)
admin.site.register(University)
admin.site.register(EmailDomain)