from django.urls import path
from .views import delete_post, delete_post_ajax

urlpatterns = [
    path('<int:post_id>/delete_post/', delete_post, name='delete_post'),
    path('delete_post_ajax/<int:post_id>/', delete_post_ajax, name='delete_post_ajax'),
]