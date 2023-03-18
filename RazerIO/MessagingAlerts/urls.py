from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from .views import inbox, outbox, conversation, delete_conversation, delete_alert

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    re_path(r'^inbox/(?P<user_id>\d+)/$', inbox, name='inbox_with_user_id'),
    path('outbox/', outbox, name='outbox'),
    path('conversation/<int:id>', conversation, name='conversation'),
    path('alerts/delete/<int:alert_id>/', delete_alert, name='delete_alert'),
    # URL for starting conversations with prepopulated users:
    path('conversation/<int:conversation_id>/delete/', delete_conversation, name='delete_conversation'),

]