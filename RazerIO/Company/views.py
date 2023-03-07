from django.shortcuts import render
from .models import Company
from operator import itemgetter
# Create your views here.

# def CompanyPage(request, id):
#     company = Company.objects.get(id=id)
#     employees = Company.objects.filter(id=id).count()
#     context = {'Company':company, 'Employees':employees}
#     return render(request, 'company.html', context=context)
def Merge(dict1, dict2):
    return (dict2.update(dict1))


import yfinance as yf
from django.utils import timezone

def CompanyPage(request, id):
    company = Company.objects.get(id=id)
    ticker = yf.Ticker(company.StockTicker)
    employees = Company.objects.filter(id=id).count()
    stock_price = ticker.fast_info['lastPrice'] if company.StockTicker else None
    market_cap = ticker.fast_info['marketCap'] if company.StockTicker else None
    institutional = ticker.institutional_holders[:5]
    mutual_funds = ticker.mutualfund_holders[:5]
    institutional = institutional.copy()
    mutual_funds = mutual_funds.copy()
    institutional.loc[:, 'Shares_M'] = institutional.loc[:, 'Shares'] / 1000000
    institutional['Value_M'] = institutional['Value'] / 1000000
    mutual_funds['Value_M'] = mutual_funds['Value'] / 1000000
    mutual_funds['Shares_M'] = mutual_funds['Shares'] / 1000000
    market_cap_M = market_cap / 1000000

    context = {
        'Company': company,
        'Employees': employees,
        'StockPrice': stock_price,
        'Institutional': institutional,
        'MutualFunds':mutual_funds,
        'MarketCap':market_cap_M
    }
    return render(request, 'company.html', context=context)
