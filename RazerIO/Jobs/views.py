from django.core.paginator import Paginator
from django.shortcuts import render
from .models import JobListing

def jobs(request):
    job_list = JobListing.objects.all().order_by('Date_Posted')
    paginator = Paginator(job_list, 10)  # Display 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    return render(request, 'jobs.html', {'jobs': jobs})
