from django.urls import path

from .views import CompanyPage, edit_company_about

urlpatterns = [
    path("<int:id>", CompanyPage, name='company'),
    path("<int:company_id>/edit/", edit_company_about, name="edit_company")
]