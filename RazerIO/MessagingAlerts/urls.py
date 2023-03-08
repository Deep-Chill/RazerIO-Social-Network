from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import inbox, outbox, conversation, alerts

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('outbox/', outbox, name='outbox'),
    path('conversation/<int:id>', conversation, name='conversation'),
    path('alerts/', alerts, name='alerts')
]