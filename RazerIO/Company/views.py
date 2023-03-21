from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, CompanyReview, user_has_verified_email, user_has_not_reviewed_company, LeadInvestor, NotablePerson
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import Http404, HttpResponseForbidden
from operator import itemgetter
from django.core.cache import cache
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import EditCompanyForm, CreatePrivateCompanyForm, CreatePublicCompanyForm, EmailDomainForm, CompanyReviewForm, LeadInvestorForm, NotablePersonForm, ValuationForm, NonEmployeeReviewForm
from .utils import fetch_company_data
import requests
from django.db import IntegrityError
from django.db.models import Avg
import json
import math
from yahooquery import Ticker
from django.core.exceptions import ValidationError
from datetime import date, timezone

current_year = date.today().year

def get_company_score(company):
    if company.Founded:
        company_age = current_year - company.Founded.year
    else:
        company_age = 0
    avg_ratings = company.reviews.aggregate(
        avg_overall_rating=Avg('overall_rating'))

    max_age_score = 100  # maximum age of a company considered for scoring

    # Weights for each factor
    weights = {
        'market_cap': 0.35,
        'employee_count': 0.15,
        'annual_revenue': 0.15,
        'annual_profit': 0.02,
        'total_liabilities': -0.02,
        'total_debt': -0.02,
        'cash_on_hand': 0.05,
        'assets': 0.05,
        'net_assets': 0.1,
        'company_founded': 0.03,
        'reviews_on_our_website': 0.03,
    }

    # Normalize news_sentiment_score to 0-1 range

    # Calculate scores for each factor
    market_cap_score = math.log10(company.MarketCap + 1) / 15 if company.MarketCap else 0
    employee_count_score = math.log10(company.EmployeeCount + 1) / 6 if company.EmployeeCount else 0
    annual_revenue_score = math.log10(company.AnnualRevenue + 1) / 12 if company.AnnualRevenue else 0
    if company.AnnualProfit is not None and company.AnnualProfit > 0:
        annual_profit_score = math.log10(company.AnnualProfit + 1) / 12
    else:
        annual_profit_score = 0
    total_liabilities_score = float(company.TotalLiabilities) / (10 ** 12) if company.TotalLiabilities else 0
    total_debt_score = float(company.TotalDebt) / (10 ** 12) if company.TotalDebt else 0
    cash_on_hand_score = float(company.CashOnHand) / (10 ** 12) if company.CashOnHand else 0
    assets_score = float(company.Assets) / (10 ** 12) if company.Assets else 0
    net_assets_score = float(company.NetAssets) / (10 ** 12) if company.NetAssets else 0
    company_founded_score = min(company_age / max_age_score, 1.0) if company.Founded else 0
    reviews_on_our_website_score = avg_ratings['avg_overall_rating'] / 5 if avg_ratings['avg_overall_rating'] else 0

    # Calculate the final company score using weights
    company_score = (
        weights['market_cap'] * market_cap_score +
        weights['employee_count'] * employee_count_score +
        weights['annual_revenue'] * annual_revenue_score +
        weights['annual_profit'] * annual_profit_score +
        weights['total_liabilities'] * total_liabilities_score +
        weights['total_debt'] * total_debt_score +
        weights['cash_on_hand'] * cash_on_hand_score +
        weights['assets'] * assets_score +
        weights['net_assets'] * net_assets_score +
        weights['company_founded'] * company_founded_score +
        weights['reviews_on_our_website'] * reviews_on_our_website_score
    )
    # cache_key = f'company_score_{company.id}'
    # cache.set(cache_key, company_score, timeout=24 * 60 * 60)

    return company_score


def update_and_cache_company_score(company):
    company_score = get_company_score(company)
    company.company_score = company_score
    company.save(update_fields=['company_score'])

    cache_key = f'company_score_{company.id}'
    cache.set(cache_key, company_score, timeout=24 * 60 * 60)


def cache_company_score(company):
    cache_key = f'company_score_{company.id}'
    score = cache.get(cache_key)
    if score is None:
        if company.company_score is not None:
            score = company.company_score
        else:
            score = get_company_score(company)
            company.company_score = score
            company.save(update_fields=['company_score'])

        cache.set(cache_key, score, timeout=24 * 60 * 60)

    return score


def update_company_score(company):
    company_score = get_company_score(company)
    company.company_score = company_score
    company.save(update_fields=['company_score'])


@cache_page(1*60*60)
def company_leaderboard(request):
    companies = Company.objects.all()
    scored_companies = []

    for company in companies:
        score = cache_company_score(company)
        scored_companies.append({'company': company, 'score': score})

    sorted_companies = sorted(scored_companies, key=lambda x: x['score'], reverse=True)

    context = {
        'sorted_companies': sorted_companies,
    }

    return render(request, 'company_leaderboard.html', context)


# Create your views here.
@cache_page(60)
def CompanyPage(request, id):
    company = get_object_or_404(Company, id=id)

    avg_ratings = company.reviews.aggregate(
        avg_overall_rating=Avg('overall_rating'),
        avg_culture_and_atmosphere_rating=Avg('culture_and_atmosphere_rating'),
        avg_senior_leadership_rating=Avg('senior_leadership_rating'),
        avg_compensation_and_benefits_rating=Avg('compensation_and_benefits_rating'),
        avg_career_opportunities_rating=Avg('career_opportunities_rating'),
        avg_work_life_balance_rating=Avg('work_life_balance_rating'),
        avg_future_outlook=Avg('future_outlook')
    )
    recent_reviews = company.reviews.order_by('-created_at')[:3]

    company_data = None
    if company.IsPublic:
        company_data = fetch_company_data(company)
        print(company_data)

    notable_people = NotablePerson.objects.select_related('company').filter(company=company)[:5]
    lead_investors = LeadInvestor.objects.select_related('content_type').filter(companies=company).order_by('-amount_invested')[:5]
    funding_rounds = company.funding_rounds.all().select_related('company')
    valuation = company.valuations.all().select_related('company')
    company_score = cache_company_score(company)

    context = {
        'Company': company,
        'NotablePeople': notable_people,
        'LeadInvestors': lead_investors,
        'FundingRounds': funding_rounds,
        'CompanyValuation': valuation,
        'avg_ratings': avg_ratings,
        'recent_reviews': recent_reviews,
        'CompanyScore': company_score
    }

    if company_data:
        company.last_updated_other_fields = timezone.now()
        company.save(update_fields=['last_updated_other_fields'])

        update_and_cache_company_score(company)  # Update company score and cache

        context.update(company_data)

    return render(request, 'company.html', context=context)


@login_required
def edit_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    user = request.user

    if not user.Company.id == company_id:
        return HttpResponseForbidden("You don't have permission to edit this company.")

    if not user.Company_Verified_Email:
        return HttpResponseForbidden("You don't have permission to edit this company.")

    form = EditCompanyForm(instance=company)
    email_domain_form = EmailDomainForm(prefix='email_domain')

    if not company.IsPublic:
        notable_person_form = NotablePersonForm(prefix='notable_person')
        lead_investor_form = LeadInvestorForm(prefix='lead_investor')
        valuation_form = ValuationForm(prefix='valuation')
    else:
        notable_person_form = lead_investor_form = valuation_form = None

    if request.method == 'POST':
        if 'edit_company_submit' in request.POST:
            form = EditCompanyForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                form.save(user=user)
                # Redirect to the company detail view or another appropriate view

        notable_person_form = NotablePersonForm(prefix='notable_person', instance=None)
        lead_investor_form = LeadInvestorForm(prefix='lead_investor', instance=None)
        valuation_form = ValuationForm(prefix='valuation', instance=None)

        if not company.IsPublic:
            if 'notable_person_submit' in request.POST:
                notable_person_form = NotablePersonForm(request.POST, prefix='notable_person')
                if notable_person_form.is_valid():
                    notable_person = notable_person_form.save(commit=False)
                    notable_person.company = company
                    notable_person.save()

            if 'lead_investor_submit' in request.POST:
                lead_investor_form = LeadInvestorForm(request.POST, prefix='lead_investor')
                if lead_investor_form.is_valid():
                    lead_investor = lead_investor_form.save()
                    lead_investor.companies.add(company)

            if 'valuation_submit' in request.POST:
                valuation_form = ValuationForm(request.POST, prefix='valuation')
                if valuation_form.is_valid():
                    valuation = valuation_form.save(commit=False)
                    valuation.company = company
                    valuation.save()

        if 'email_domain_submit' in request.POST:
            email_domain_form = EmailDomainForm(request.POST, prefix='email_domain')
            if email_domain_form.is_valid():
                email_domain = email_domain_form.save()
                company.Email_Domain.add(email_domain)

    context = {
        'form': form,
        'email_domain_form': email_domain_form,
    }

    if not company.IsPublic:
        context.update({
            'company':company,
            'notable_person_form': notable_person_form,
            'lead_investor_form': lead_investor_form,
            'valuation_form': valuation_form,
        })

    return render(request, 'edit_company_about.html', context)


def create_company(request):
    public_company_form = CreatePublicCompanyForm()
    private_company_form = CreatePrivateCompanyForm()
    email_domain_form = EmailDomainForm()

    if request.method == 'POST':
        print("POST request received")
        if 'public_form_submit' in request.POST:
            print("Public form submitted")
            company_form = CreatePublicCompanyForm(request.POST)
            email_domain_form = EmailDomainForm(request.POST)
            company_form.instance.IsPublic = True
        elif 'private_form_submit' in request.POST:
            print("Private form submitted")
            company_form = CreatePrivateCompanyForm(request.POST, request.FILES)
            email_domain_form = EmailDomainForm(request.POST)
            company_form.instance.StockTicker = None
            company_form.instance.IsPublic = False
        else:
            print("No form submitted")
            company_form = None
            # email_domain_form = None

        if company_form:
            print("Company form exists")
            if 'public_form_submit' in request.POST:
                print("Checking validity for public form")
                is_valid = email_domain_form.is_valid() and company_form.is_valid()
            else:
                print("Checking validity for private form")
                is_valid = email_domain_form.is_valid() and company_form.is_valid()

            if is_valid:
                print("Form is valid")
                company = company_form.save(commit=False)
                if isinstance(company_form, CreatePublicCompanyForm):
                    print("Saving public company")
                    is_public = True
                    stock_ticker = request.POST.get('StockTicker')
                    company_data = fetch_company_data(company, is_new=True)
                else:
                    print("Saving private company")
                    is_public = False
                company.IsPublic = is_public
                company.save()

                email_domain = email_domain_form.save(commit=False)
                email_domain.save()

                # Add the new email domain to the company
                company.Email_Domain.add(email_domain)

                return redirect('company', id=company.id)
            else:
                print("Form is not valid")
                print("Company form errors:")
                for field, error in company_form.errors.items():
                    print(f"{field}: {error}")
                print("Email domain form errors:")
                for field, error in email_domain_form.errors.items():
                    print(f"{field}: {error}")
                for field, error in company_form.errors.items():
                    messages.error(request, f"{field}: {error}")
                for field, error in email_domain_form.errors.items():
                    messages.error(request, f"{field}: {error}")
                return redirect('create_company')

    context = {
        'public_company_form': public_company_form,
        'private_company_form': private_company_form,
        'email_domain_form_public': email_domain_form,
        'email_domain_form_private': email_domain_form,
    }
    return render(request, 'create_company.html', context=context)


def company_reviews(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    reviews = company.reviews.all()

    paginator = Paginator(reviews, 25) # Show 25 reviews per page
    page = request.GET.get('page')
    paged_reviews = paginator.get_page(page)

    context = {
        'company': company,
        'reviews': reviews,
    }
    return render(request, 'company_reviews.html', context)

def create_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = CompanyReviewForm(request.POST)
        if form.is_valid():
            user = request.user
            if user_has_verified_email(user, company):
                if user_has_not_reviewed_company(user, company):
                    review = form.save(commit=False)
                    review.company = company
                    review.user_email_domain = user.email.split("@")[-1]
                    try:
                        review.save()
                    except IntegrityError:
                        messages.error(request, "You have already submitted a review for this company.")
                        return render(request, 'create_employee_review.html', {'form': form, 'company': company})
                    return redirect('company_reviews', company_id=company.id)
                else:
                    messages.error(request, 'You have already reviewed this company.')
            else:
                messages.error(request, 'You need to verify your company email before posting a review.')
    else:
        form = CompanyReviewForm()

    return render(request, 'create_employee_review.html', {'form': form, 'company': company})

def review_detail(request, review_id):
    review = get_object_or_404(CompanyReview, id=review_id)
    return render(request, 'review_detail.html', {'review': review})

def edit_history(request, company_id):
    company = Company.objects.get(id=company_id)
    edit_history = company.edit_history.all().order_by('-timestamp')

    # Deserialize the changes field for each history item
    for history_item in edit_history:
        history_item.changes = json.loads(history_item.changes)

    context = {
        'company': company,
        'edit_history': edit_history,
    }

    return render(request, 'edit_history.html', context)


def create_non_employee_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = NonEmployeeReviewForm(request.POST)
        if form.is_valid():
            user = request.user
            review = form.save(commit=False)
            review.company = company
            review.user = user
            review.save()
            return redirect('company_reviews', company_id=company.id)
    else:
        form = NonEmployeeReviewForm()

    return render(request, 'create_non_employee_review.html', {'form': form, 'company': company})
