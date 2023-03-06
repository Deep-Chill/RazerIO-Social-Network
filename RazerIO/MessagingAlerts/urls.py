from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import inbox

urlpatterns = [
    path('messages/', inbox, name='inbox'),
]
