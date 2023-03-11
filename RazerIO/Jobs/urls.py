from django.urls import path
from .views import jobs, JobPosting, CreateJobListing, MyJobPosts, ApplyToJob, MyJobApplications, job_applicants, delete_application

urlpatterns = [
    path('jobs/', jobs, name='jobs'),
    path('jobs/<int:id>/', JobPosting, name='jobposting'),
    path('job-listings/create/', CreateJobListing, name='createjoblisting'),
    path('myjobposts/', MyJobPosts, name='myjobposts'),
    path('jobs/<int:id>/apply/', ApplyToJob, name='apply_to_job'),
    path('jobs/myapplications/', MyJobApplications, name='job_applications'),
    path('jobs/<int:job_id>/applicants/', job_applicants, name='job_applicants'),
    path('job/myapplications/delete/<int:application_id>/', delete_application, name='delete_job_application'),
]
