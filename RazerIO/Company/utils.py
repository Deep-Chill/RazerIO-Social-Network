from yahooquery import Ticker
import pandas as pd
import numpy as np
from django.core.cache import cache
from .models import Company, LeadInvestor, NotablePerson
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType


def fetch_yahoo_data(stock_ticker):
    ticker = Ticker(stock_ticker)

    try:
        if not ticker.summary_profile or not isinstance(ticker.summary_profile.get(stock_ticker, None), dict):
            return None
    except Exception as e:
        print(f"Error fetching data for stock ticker {stock_ticker}: {e}")
        return None

    # Wrap each block of data retrieval in a try-except block to handle any potential exceptions
    try:
        financial_data = ticker.financial_data.get(stock_ticker, {})
        summary_detail = ticker.summary_detail.get(stock_ticker, {})
        summary_profile = ticker.summary_profile.get(stock_ticker, {})
        earnings_data = ticker.earnings.get(stock_ticker, {})
        balance_sheet_data = ticker.balance_sheet(frequency='a')
        income_statement_data = ticker.income_statement(frequency='a')
    except Exception as e:
        print(f"Error fetching financial data for stock ticker {stock_ticker}: {e}")
        return None

    if not balance_sheet_data.empty:
        balance_sheet = balance_sheet_data.loc[balance_sheet_data.index.get_level_values('symbol') == stock_ticker].iloc[0]
    else:
        balance_sheet = {}

    institutional_ownership = ticker.institution_ownership
    institutional_ownership_df = pd.DataFrame(institutional_ownership, columns=['organization', 'pctHeld', 'position', 'value'])

    major_holders = ticker.major_holders.get(stock_ticker, [])

    fund_ownership = ticker.fund_ownership
    mutual_fund_holders_df = pd.DataFrame(fund_ownership, columns=['organization', 'pctHeld', 'position', 'value'])

    merged_ownership_df = pd.concat([institutional_ownership_df, mutual_fund_holders_df]).fillna(value=np.nan)
    merged_ownership_df.sort_values(by='position', ascending=False, inplace=True)

    top_5_owners = merged_ownership_df.head(5).to_dict(orient='records')

    company_officers = ticker.company_officers
    company_officers_df = pd.DataFrame(company_officers, columns=['name', 'age', 'title', 'yearBorn', 'totalPay']).head(5).fillna(value=np.nan)

    try:
        yearly_financials = earnings_data.get('financialsChart', {}).get('yearly', [])
        annual_revenue = yearly_financials[-1]['revenue'] if yearly_financials else None
        annual_profit = yearly_financials[-1]['earnings'] if yearly_financials else None
    except (AttributeError, IndexError):
        annual_revenue, annual_profit = None, None

    if not (isinstance(financial_data, dict) and isinstance(summary_detail, dict) and isinstance(summary_profile, dict) and isinstance(earnings_data, dict) and isinstance(balance_sheet, pd.Series)):
        return None

    # Use dict.get() to avoid KeyError exceptions
    company_data = {
        'StockPrice': financial_data.get('currentPrice', None),
        'MarketCap': summary_detail.get('marketCap', None),
        'EmployeeCount': summary_profile.get('fullTimeEmployees', None),
        'LongBusinessSummary': summary_profile.get('longBusinessSummary', ''),
        'InstitutionalOwnership': institutional_ownership_df.to_dict(orient='records') if institutional_ownership_df is not None else [],
        'MajorHolders': major_holders if major_holders is not None else [],
        'Top5Owners': top_5_owners if top_5_owners is not None else [],
        'CompanyOfficers': company_officers_df.to_dict(orient='records') if company_officers_df is not None else [],
        'AnnualRevenue': annual_revenue if annual_revenue is not None else None,
        'AnnualProfit': annual_profit if annual_profit is not None else None,
        'Website': summary_profile.get('website', ''),
        'Headquarters': summary_profile.get('city', ''),
        'Country': summary_profile.get('country', ''),
        'TotalLiabilities': balance_sheet.get('CurrentLiabilities', None),
        'TotalDebt': balance_sheet.get('TotalDebt', None),
        'CashOnHand': balance_sheet.get('CashAndCashEquivalents', None),
        'Assets': balance_sheet.get('CurrentAssets', None),
        'NetAssets': balance_sheet['CurrentAssets'] - balance_sheet['CurrentLiabilities'] if 'CurrentAssets' in balance_sheet and 'CurrentLiabilities' in balance_sheet else None,
    }

    return company_data


def fetch_stock_price_and_market_cap(stock_ticker):
    try:
        ticker = Ticker(stock_ticker)
        summary_detail = ticker.summary_detail.get(stock_ticker, {})
        financial_data = ticker.financial_data.get(stock_ticker, {})
        if not (isinstance(summary_detail, dict) and isinstance(financial_data, dict)):
            return None
    except Exception as e:
        print(f"Error fetching data for stock ticker {stock_ticker}: {e}")
        return None

    stock_price = round(financial_data.get('currentPrice', 0))
    market_cap = round(summary_detail.get('marketCap', 0))
    return {'StockPrice': stock_price, 'MarketCap': market_cap}


def fetch_company_data(company, is_new=False):
    current_time = timezone.now()

    update_stock_price_and_market_cap = is_new or (current_time - company.last_updated_stockdata) >= timedelta(days=1)
    update_other_fields = is_new or (current_time - company.last_updated_other_fields) >= timedelta(days=30)

    if update_stock_price_and_market_cap:
        stock_data = fetch_stock_price_and_market_cap(company.StockTicker)
        if stock_data:
            company.StockPrice = stock_data['StockPrice']
            company.MarketCap = stock_data['MarketCap']
            company.last_updated_stock_data = current_time
            company.save()

    if update_other_fields:
        other_data = fetch_yahoo_data(company.StockTicker)
        if other_data:
            company.EmployeeCount = round(other_data['EmployeeCount']) if other_data['EmployeeCount'] is not None else None
            company.LongBusinessSummary = other_data['LongBusinessSummary']
            company.AnnualRevenue = round(other_data['AnnualRevenue']) if other_data['AnnualRevenue'] is not None else None
            company.AnnualProfit = round(other_data['AnnualProfit']) if other_data['AnnualProfit'] is not None else None
            company.Headquarters = other_data['Headquarters']
            company.Country = other_data['Country']
            company.TotalLiabilities = round(other_data['TotalLiabilities']) if other_data['TotalLiabilities'] is not None else None
            company.TotalDebt = round(other_data['TotalDebt']) if other_data['TotalDebt'] is not None else None
            company.CashOnHand = round(other_data['CashOnHand']) if other_data['CashOnHand'] is not None else None
            company.Assets = round(other_data['Assets']) if other_data['Assets'] is not None else None
            company.NetAssets = round(other_data['NetAssets']) if other_data['NetAssets'] is not None else None
            company.About = other_data['LongBusinessSummary']
            company.Website = other_data['Website']

            for owner in other_data['Top5Owners']:
                lead_investor, created = LeadInvestor.objects.update_or_create(
                    name=owner['organization'],
                    content_type=ContentType.objects.get_for_model(LeadInvestor),
                    object_id=company.id,
                    defaults={
                        'amount_invested': owner['value'],
                        'bio': '',
                        'website': ''
                    }
                )
                if created:
                    lead_investor.companies.add(company)
                    lead_investor.save()

            # Adding company officers as NotablePerson
            for officer in other_data['CompanyOfficers']:
                age = int(officer['age']) if not np.isnan(officer['age']) else None
                salary = int(officer['totalPay']) if not np.isnan(officer['totalPay']) else None

                NotablePerson.objects.update_or_create(
                    name=officer['name'],
                    content_type=ContentType.objects.get_for_model(NotablePerson),
                    object_id=company.pk,
                    defaults={
                        'title': officer['title'],
                        'achievements': '',
                        'company': company,
                        'salary': salary,
                        'age': age
                    }
                )
            company.last_updated_other_fields = current_time
            company.save()
