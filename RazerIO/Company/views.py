from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, CompanyReview, user_has_verified_email, user_has_not_reviewed_company
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import Http404, HttpResponseForbidden
from operator import itemgetter
from django.core.cache import cache
from django.contrib import messages
from .forms import EditCompanyForm, CreateCompanyForm, EmailDomainForm, CompanyReviewForm, LeadInvestorForm, NotablePersonForm, ValuationForm
from .utils import fetch_company_data
import requests
from django.db import IntegrityError
from django.db.models import Avg
import json

# Create your views here.

def Merge(dict1, dict2):
    return (dict2.update(dict1))

def CompanyPage(request, id):
    company = Company.objects.get(id=id)
    avg_ratings = company.reviews.aggregate(
        avg_overall_rating=Avg('overall_rating'),
        avg_culture_and_values_rating=Avg('culture_and_values_rating'),
        avg_senior_leadership_rating=Avg('senior_leadership_rating'),
        avg_compensation_and_benefits_rating=Avg('compensation_and_benefits_rating'),
        avg_career_opportunities_rating=Avg('career_opportunities_rating'),
        avg_work_life_balance_rating=Avg('work_life_balance_rating'),
        avg_future_outlook=Avg('future_outlook')
    )
    recent_reviews = company.reviews.order_by('-created_at')[:3]
    company_data = fetch_company_data(company.StockTicker, company.Name, company.IsPublic)
    notable_people = company.notable_people.all()
    lead_investors = company.lead_investors.all()
    funding_rounds = company.funding_rounds.all()
    valuation = company.valuations.all()
    context = {
        'Company': company,
        'StockPrice': company_data.get('StockPrice'),
        'MarketCap': company_data.get('MarketCap'),
        'EmployeeCount': company_data.get('EmployeeCount'),
        'LongBusinessSummary': company_data.get('LongBusinessSummary'),
        'CompanyOfficers': company_data.get('CompanyOfficers'),
        'InstitutionalOwnership': company_data.get('InstitutionalOwnership'),
        'MajorHolders': company_data.get('MajorHolders'),
        'Top3Owners': company_data.get('Top3Owners'),
        'AnnualRevenue': company_data.get('AnnualRevenue'),
        'AnnualProfit': company_data.get('AnnualProfit'),
        'NotablePeople': notable_people,
        'LeadInvestors': lead_investors,
        'FundingRounds': funding_rounds,
        'CompanyValuation': valuation,
        'avg_ratings': avg_ratings,
        'recent_reviews': recent_reviews
    }
    return render(request, 'company.html', context=context)


@login_required
def edit_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    user = request.user

    if not user.Company.id == company_id:
        return HttpResponseForbidden("You don't have permission to edit this company.")

    if not user.Company_Verified_Email:
        return HttpResponseForbidden("You don't have permission to edit this company.")
    print(user.Company)

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
            'notable_person_form': notable_person_form,
            'lead_investor_form': lead_investor_form,
            'valuation_form': valuation_form,
        })

    return render(request, 'edit_company_about.html', context)



def create_company(request):
    if request.method == 'POST':
        company_form = CreateCompanyForm(request.POST, request.FILES)
        email_domain_form = EmailDomainForm(request.POST)

        if company_form.is_valid() and email_domain_form.is_valid():
            company = company_form.save()
            email_domain = email_domain_form.save(commit=False)
            email_domain.company = company
            email_domain.save()

            return redirect('company_detail', company_id=company.pk)

    else:
        company_form = CreateCompanyForm()
        email_domain_form = EmailDomainForm()
    context = {'company_form': company_form, 'email_domain_form': email_domain_form}
    return render(request, 'create_company.html', context=context)

def company_reviews(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    reviews = company.reviews.all()

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
                        return render(request, 'create_review.html', {'form': form, 'company': company})
                    return redirect('company_reviews', company_id=company.id)
                else:
                    messages.error(request, 'You have already reviewed this company.')
            else:
                messages.error(request, 'You need to verify your company email before posting a review.')
    else:
        form = CompanyReviewForm()

    return render(request, 'create_review.html', {'form': form, 'company': company})

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
