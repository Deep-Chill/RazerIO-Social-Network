from django.urls import path

from .views import endorsement

urlpatterns = [
    path("", endorsement, name='endorsement')
]