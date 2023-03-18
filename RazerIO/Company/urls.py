from django.urls import path

from .views import CompanyPage, edit_company, create_company, company_reviews, create_review, review_detail, edit_history, create_non_employee_review, company_leaderboard

urlpatterns = [
    path("<int:id>", CompanyPage, name='company'),
    path("<int:company_id>/edit/", edit_company, name="edit_company"),
    path("create_company", create_company, name="create_company"),
    path('reviews/<int:company_id>/', company_reviews, name='company_reviews'),
    path('reviews/<int:company_id>/create/employee', create_review, name='create_employee_review'),
    path('read_review/<int:review_id>/', review_detail, name='review_detail'),
    path('<int:company_id>/edit_history', edit_history, name='edit_history'),
    path('reviews/<int:company_id>/create/non_employee', create_non_employee_review, name='create_non_employee_review'),
    path('leaderboard/', company_leaderboard, name='company_leaderboard'),

]