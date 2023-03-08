from django.urls import path

from .views import endorsement

urlpatterns = [
    path("<int:id>", endorsement, name='endorsement')
]