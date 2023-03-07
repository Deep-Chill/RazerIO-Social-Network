from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import inbox, outbox

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('outbox/', outbox, name='outbox')
]