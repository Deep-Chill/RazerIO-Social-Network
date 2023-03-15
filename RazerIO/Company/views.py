from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import Http404
from operator import itemgetter
from django.core.cache import cache
from django.contrib import messages
from .forms import EditCompanyAboutForm
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

def fetch_company_data(stock_ticker):
    data = cache.get(stock_ticker)
    if data is None:
        ticker = yf.Ticker(stock_ticker)
        stock_price = ticker.fast_info['lastPrice']
        market_cap = ticker.fast_info['marketCap']
        institutional = ticker.institutional_holders[:5]
        mutual_funds = ticker.mutualfund_holders[:5]

        data = {
            'StockPrice': stock_price,
            'MarketCap': market_cap,
            'Institutional': institutional,
            'MutualFunds': mutual_funds,
        }
        cache.set(stock_ticker, data, 60 * 15)  # Cache data for 15 minutes

    return data


def CompanyPage(request, id):
    company = Company.objects.get(id=id)
    employees = Company.objects.filter(id=id).count()
    if company.StockTicker:
        company_data = fetch_company_data(company.StockTicker)
        stock_price = company_data['StockPrice']
        market_cap = company_data['MarketCap']
        institutional = company_data['Institutional']
        mutual_funds = company_data['MutualFunds']
    else:
        stock_price = None
        market_cap = None
        institutional = None
        mutual_funds = None
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
        'MarketCap':market_cap_M,
    }
    return render(request, 'company.html', context=context)


@login_required
def edit_company_about(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.user.Company != company:
        raise Http404

    if request.method == 'POST':
        form = EditCompanyAboutForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.LastEditedBy = request.user
            company.save()
            messages.success(request, 'Company About section updated successfully.')
            return redirect('company', id=company.id)
    else:
        form = EditCompanyAboutForm(instance=company)

    return render(request, 'edit_company_about.html', {'form': form, 'company': company})
