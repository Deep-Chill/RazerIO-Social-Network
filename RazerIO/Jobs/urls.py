from django.urls import path
from .views import jobs, JobPosting, CreateJobListing, MyJobPosts, ApplyToJob, MyJobApplications, job_applicants, delete_application, jobPostingbycompany, edit_job_listing

urlpatterns = [
    path('jobs/', jobs, name='jobs'),
    path('jobs/<int:id>/', JobPosting, name='jobposting'),
    path('job-listings/create/', CreateJobListing, name='createjoblisting'),
    path('myjobposts/', MyJobPosts, name='myjobposts'),
    path('jobs/<int:id>/apply/', ApplyToJob, name='apply_to_job'),
    path('jobs/myapplications/', MyJobApplications, name='job_applications'),
    path('jobs/<int:job_id>/applicants/', job_applicants, name='job_applicants'),
    path('job/myapplications/delete/<int:application_id>/', delete_application, name='delete_job_application'),
    path('jobs/company/<int:id>', jobPostingbycompany, name='job_posting_by_company'),
    path('job-listings/edit/<int:id>/', edit_job_listing, name='edit_job_listing'),
]

# urlpatterns = [
#     # Job listings and details
#     path('jobs/', views.jobs, name='jobs'),
#     path('jobs/<int:id>/', views.JobPosting, name='jobposting'),
#     path('jobs/company/<int:id>/', views.jobPostingbycompany, name='job_posting_by_company'),
#
#     # Job applications
#     path('jobs/<int:id>/apply/', views.ApplyToJob, name='apply_to_job'),
#     path('jobs/myapplications/', views.MyJobApplications, name='job_applications'),
#     path('jobs/myapplications/delete/<int:application_id>/', views.delete_application, name='delete_job_application'),
#
#     # Job postings management
#     path('job-listings/create/', views.CreateJobListing, name='createjoblisting'),
#     path('job-listings/my/', views.MyJobPosts, name='myjobposts'),
#     path('job-listings/edit/<int:id>/', views.edit_job_listing, name='edit_job_listing'),
#
#     # Job applicants
#     path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
# ]
