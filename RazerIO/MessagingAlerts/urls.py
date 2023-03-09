from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import inbox, outbox, conversation, alerts, start_new_conversation

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('outbox/', outbox, name='outbox'),
    path('conversation/<int:id>', conversation, name='conversation'),
    path('alerts/', alerts, name='alerts'),
    path('new_conversation/', start_new_conversation, name='new_conversation'),
    path('new_conversation/<int:user_id>/', start_new_conversation, name='new_conversation_id'),

]