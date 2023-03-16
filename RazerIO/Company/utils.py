from yahooquery import Ticker
import pandas as pd
from django.core.cache import cache

def fetch_yahoo_data(stock_ticker):
    ticker = Ticker(stock_ticker)
    financial_data = ticker.financial_data[stock_ticker]
    summary_detail = ticker.summary_detail[stock_ticker]
    summary_profile = ticker.summary_profile[stock_ticker]
    earnings_data = ticker.earnings[stock_ticker]

    # Institutional ownership
    institutional_ownership = ticker.institution_ownership
    institutional_ownership_df = pd.DataFrame(institutional_ownership, columns=['organization', 'pctHeld', 'position', 'value'])

    # Major holders
    major_holders = ticker.major_holders[stock_ticker]

    # Mutual fund holders
    fund_ownership = ticker.fund_ownership
    mutual_fund_holders_df = pd.DataFrame(fund_ownership, columns=['organization', 'pctHeld', 'position', 'value'])

    # Merge institutional ownership and mutual fund holders data
    merged_ownership_df = pd.concat([institutional_ownership_df, mutual_fund_holders_df])
    merged_ownership_df.sort_values(by='position', ascending=False, inplace=True)

    # Get the top 3 owners
    top_3_owners = merged_ownership_df.head(5).to_dict(orient='records')

    company_officers = ticker.company_officers
    company_officers_df = pd.DataFrame(company_officers, columns=['name', 'age', 'title', 'yearBorn', 'fiscalYear', 'totalPay', 'exercisedValue', 'unexercisedValue']).head(5)

    yearly_financials = earnings_data['financialsChart']['yearly']
    annual_revenue = yearly_financials[-1]['revenue']  # Get the latest year's revenue
    annual_profit = yearly_financials[-1]['earnings']  # Get the latest year's earnings

    company_data = {
        'StockPrice': financial_data['currentPrice'],
        'MarketCap': summary_detail['marketCap'],
        'EmployeeCount': summary_profile['fullTimeEmployees'],
        'LongBusinessSummary': summary_profile['longBusinessSummary'],
        'CompanyOfficers': summary_profile['companyOfficers'],
        'InstitutionalOwnership': institutional_ownership_df.to_dict(orient='records'),
        'MajorHolders': major_holders,
        'Top3Owners': top_3_owners,
        'CompanyOfficers': company_officers_df.to_dict(orient='records'),
        'AnnualRevenue': annual_revenue,
        'AnnualProfit': annual_profit,
    }
    return company_data

def fetch_company_data(stock_ticker, company_name, is_public=True):
    company_data = cache.get(stock_ticker)

    if company_data is None:
        company_data = {
            'StockPrice': None,
            'MarketCap': None,
            'EmployeeCount': None,
            'Industry': None,
            'Sector': None,
            'LongBusinessSummary': None,
            'CompanyOfficers': None,
            'InstitutionalOwnership': None,
            'MajorHolders': None,
            'Top3Owners': None,
            'LastFundingRound': None,
            'AmountRaised': None,
            'Valuation': None
        }

        if is_public:
            yahoo_data = fetch_yahoo_data(stock_ticker)
            company_data.update(yahoo_data)

    cache.set(stock_ticker, company_data, 3600)

    return company_data
