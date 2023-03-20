from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing, JobApplication, Job_Categories
from .forms import JobPosting as JP
from .forms import ApplyToJobForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Q, Func, OuterRef, Subquery, FloatField, TextField, Value, CharField, Sum, Case, When, IntegerField, ExpressionWrapper
from django.db.models.functions import Cast, Concat
from .filters import JobFilter
from django.contrib import messages
from django.core import cache
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views import View
from Company.models import Company
from django.utils import timezone
from datetime import timedelta
from Company.views import cache_company_score
from .custom_aggregates import CacheCompanyScore


def generate_alias(category_id):
    return 'category_' + ''.join(e for e in category_id if e.isalnum()) + '_count'



# @cache_page(60*60)
# def jobs(request):
#     job_listings = JobListing.objects.filter(Job_Status='Open')
#
#     top_categories_subquery = JobListing.objects.filter(
#         Company=OuterRef('Company')
#     ).annotate(
#         location=Cast('Category', output_field=CharField())
#     ).values(
#         'Category'
#     ).annotate(
#         count=Count('id')
#     ).order_by('-count')
#
#     top_locations_subquery = JobListing.objects.filter(
#         Company=OuterRef('Company')
#     ).annotate(
#         location=Cast('Location', output_field=CharField())
#     ).values(
#         'location'
#     ).annotate(
#         count=Count('id')
#     ).order_by('-count')
#
#     jobs_by_company = job_listings.values('Company__id', 'Company__Name', 'Company__company_score').annotate(
#         top_locations=Concat(
#             Subquery(top_locations_subquery.values('Location')),
#             Value(', ')
#         ),
#         top_categories=Concat(
#             Subquery(top_categories_subquery.values('Category')),
#             Value(', ')
#         ),
#         total_jobs=Count('id'),
#         company_score=F('Company__company_score'),
#     )
#
#     context = {
#         'jobs_by_company': jobs_by_company,
#     }
#
#     return render(request, 'jobs2.html', context=context)


def jobs(request):

    job_list = JobListing.objects.all()
    job_filter = JobFilter(request.GET, queryset=job_list)
    filtered_jobs_queryset = job_filter.qs


    job_posts_by_me = JobListing.objects.filter(Poster=request.user).exists()
    job_applications_by_me = JobApplication.objects.filter(applicant=request.user).values_list('job_listing', flat=True)

    return render(request, 'jobs2.html', {
        'job_posts_by_me': job_posts_by_me,
        'job_applications_by_me': job_applications_by_me,
         'jobs': job_list,
        'job_filter':job_filter,
        'filtered_jobs_queryset':filtered_jobs_queryset
    })

def jobPostingbycompany(request, id):
    company = Company.objects.get(id=id)
    salary_min = request.GET.get('salary_min', 0)
    salary_max = request.GET.get('salary_max', 9999999999)
    date_posted = request.GET.get('date_posted', None)
    job_list = JobListing.objects.filter(Job_Status='Open', Company=company)

    if salary_min:
        try:
            salary_min = float(salary_min)  # Convert salary_min to a float
            job_list = job_list.filter(salary_min__gte=salary_min)
        except ValueError:
            pass  # Ignore invalid salary_min input

    if str(salary_max) != '9999999999':  # Convert salary_max to a string when comparing
        try:
            salary_max = float(salary_max)  # Convert salary_max to a float
            job_list = job_list.filter(salary_max__lte=salary_max)
        except ValueError:
            pass  # Ignore invalid salary_max input

    if date_posted:
        days = int(date_posted)
        date_threshold = timezone.now() - timedelta(days=days)
        job_list = job_list.filter(Date_Posted__gte=date_threshold)


    job_list = job_list.order_by('Date_Posted').annotate(total_applicants=Count('jobapplication'))

    paginator = Paginator(job_list, 10)  # Display 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    job_posts_by_me = JobListing.objects.filter(Poster=request.user).exists()
    job_applications_by_me = JobApplication.objects.filter(applicant=request.user).values_list('job_listing', flat=True)
    jobs_by_company = JobListing.objects.values('Company').annotate(
        company_jobs=F('id'),
        company_name=F('Company__Name')
    ).order_by('company_name')
    job_filter = JobFilter(request.GET, queryset=job_list)
    job = job_filter.qs



    context = {
        'job_posts_by_me': job_posts_by_me,
        'jobs_by_company': jobs_by_company,
        'job_applications_by_me': job_applications_by_me,
        'job_filter': job_filter,
         'jobs': jobs,
        'job':job,
        'id':id,
        'company':company
               }
    return render(request, 'jobs_by_company.html', context=context)

def JobPosting(request, id):
    job = JobListing.objects.get(id=id)
    context = {
        'job':job
    }
    return render(request, 'jobposting.html', context=context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def CreateJobListing(request):
    if not request.user.Company_Verified_Email:
        messages.error(request, 'You need to verify your company email before creating a job listing.')
        return redirect('account_email')

    if request.method == "POST":
        form = JP(request.POST, user=request.user)
        if form.is_valid():
            company = form.cleaned_data.get('Company')
            existing_job_listing = JobListing.objects.filter(Company=company).first()

            if existing_job_listing:
                messages.error(request, f'A job listing already exists for {company}. Please edit the existing listing.')
                return redirect('edit_job_listing', id=existing_job_listing.id)

            job_listing = form.save(commit=False)
            job_listing.Poster = request.user
            job_listing.save()
            form.save_m2m()
            return redirect('jobs')
    else:
        form = JP(user=request.user)
    context = {'form': form}
    return render(request, 'postajob.html', context=context)

def edit_job_listing(request, id):
    # Implement the view logic here
    pass


def MyJobPosts(request):
    user = request.user
    job_posts_by_me = JobListing.objects.filter(Poster=user)
    context = {"job_posts_by_me":job_posts_by_me}
    return render(request, 'myjobposts.html', context=context)

def ApplyToJob(request, id):
    user = request.user
    job_listing = get_object_or_404(JobListing, id=id)
    if request.method == "POST":
        form = ApplyToJobForm(request.POST)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.applicant = user
            job_application.job_listing = job_listing
            job_application.save()
            return redirect('jobs')
    else:
        form = ApplyToJobForm()
    context = {'form':form, 'job_listing':job_listing}
    return render(request, 'apply_to_job.html', context=context)

def MyJobApplications(request):
    user = request.user
    job_applications = JobApplication.objects.filter(applicant=user)
    context = {'job_applications':job_applications}
    return render(request, 'myjobapplications.html', context=context)

def job_applicants(request, job_id):
    job_listing = get_object_or_404(JobListing, id=job_id)
    job_applications = JobApplication.objects.filter(job_listing=job_listing)

    # Add any additional sorting or filtering here
    context = {
        'job_listing': job_listing,
        'job_applications': job_applications
    }
    return render(request, 'view_job_applicants.html', context)

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Check if user has permission to delete application
    if application.applicant != request.user:
        raise PermissionDenied

    # Delete application
    application.delete()

    # Redirect to success page
    return redirect('job_applications')
