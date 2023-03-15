from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing, JobApplication
from .forms import JobPosting as JP
from .forms import ApplyToJobForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .filters import JobFilter
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from Company.models import Company
from django.db.models import Q


def jobs(request):
    salary_min = request.GET.get('salary_min', 0)
    salary_max = request.GET.get('salary_max', 9999999999)

    job_list = JobListing.objects.filter(Job_Status='Open')

    if salary_min:
        job_list = job_list.filter(salary_min__gte=salary_min)

    if str(salary_max) != '9999999999':  # Convert salary_max to a string when comparing
        job_list = job_list.filter(salary_max__lte=salary_max)

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


    return render(request, 'jobs.html', {
        'job_posts_by_me': job_posts_by_me,
        'jobs_by_company': jobs_by_company,
        'job_applications_by_me': job_applications_by_me,
        'job_filter': job_filter,
         'jobs': jobs,
        'job':job
    })

def JobPosting(request, id):
    job = JobListing.objects.get(id=id)
    context = {
        'job':job
    }
    return render(request, 'jobposting.html', context=context)

def CreateJobListing(request):
    if not request.user.Company_Verified_Email:
        #### Change this code and show an error page instead with a link to verifying your email
        messages.error(request, 'You need to verify your company email before creating a job listing.')
        return redirect('account_email')

    if request.method == "POST":
        form = JP(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.Poster = request.user
            job_listing.save()
            return redirect('jobs')
    else:
        form = JP()
    context = {'form':form}
    return render(request, 'postajob.html', context=context)

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
