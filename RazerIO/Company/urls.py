from django.urls import path

from .views import CompanyPage

urlpatterns = [
    path("<int:id>", CompanyPage, name='company')
]