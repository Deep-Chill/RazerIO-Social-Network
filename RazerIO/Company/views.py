from django.shortcuts import render
from .models import Company
# Create your views here.

# def CompanyPage(request, id):
#     company = Company.objects.get(id=id)
#     employees = Company.objects.filter(id=id).count()
#     context = {'Company':company, 'Employees':employees}
#     return render(request, 'company.html', context=context)

from yahoo_fin import stock_info
from django.utils import timezone

def CompanyPage(request, id):
    company = Company.objects.get(id=id)
    employees = Company.objects.filter(id=id).count()
    stock_price = stock_info.get_live_price(company.StockTicker) if company.StockTicker else None
    context = {'Company': company, 'Employees': employees, 'StockPrice': stock_price}
    return render(request, 'company.html', context=context)
