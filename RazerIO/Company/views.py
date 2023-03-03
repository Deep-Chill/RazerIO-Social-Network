from django.shortcuts import render
from .models import Company
# Create your views here.

def CompanyPage(request, id):
    company = Company.objects.get(id=id)
    employees = Company.objects.filter(id=id).count()
    context = {'Company':company, 'Employees':employees}
    return render(request, 'company.html', context=context)