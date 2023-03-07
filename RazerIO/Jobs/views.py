from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing, JobApplication
from .forms import JobPosting as JP
from .forms import ApplyToJobForm

def jobs(request):
    job_list = JobListing.objects.all().order_by('Date_Posted')
    paginator = Paginator(job_list, 10)  # Display 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    job_posts_by_me = JobListing.objects.filter(Poster=request.user).exists()
    return render(request, 'jobs.html', {'jobs': jobs, 'job_posts_by_me':
                                         job_posts_by_me})

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
            return redirect('jobposting', id=job_listing.id)
    else:
        form = ApplyToJobForm()
    context = {'form':form, 'job_listing':job_listing}
    return render(request, 'apply_to_job.html', context=context)

def MyJobApplications(request):
    user = request.user
    job_applications = JobApplication.objects.filter(applicant=user)
    context = {'job_applications':job_applications}
    return render(request, 'myjobapplications.html', context=context)