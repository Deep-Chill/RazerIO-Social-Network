from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing, JobApplication
from .forms import JobPosting as JP
from .forms import ApplyToJobForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count


def jobs(request):
    job_list = JobListing.objects.filter(Job_Status='Open').order_by('Date_Posted').annotate(total_applicants=Count('jobapplication'))
    paginator = Paginator(job_list, 10)  # Display 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    job_posts_by_me = JobListing.objects.filter(Poster=request.user).exists()
    job_applications_by_me = JobApplication.objects.filter(applicant=request.user).values_list('job_listing', flat=True)
    # Group jobs by company
    jobs_by_company = JobListing.objects.values('Company').annotate(
        company_jobs=F('id'),
        company_name=F('Company__Name')
    ).order_by('company_name')

    return render(request, 'jobs.html', {
        'jobs': jobs,
        'job_posts_by_me': job_posts_by_me,
        'jobs_by_company': jobs_by_company,
        'job_applications_by_me': job_applications_by_me
    })

def JobPosting(request, id):
    job = JobListing.objects.get(id=id)
    context = {
        'job':job
    }
    return render(request, 'jobposting.html', context=context)

def CreateJobListing(request):
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
