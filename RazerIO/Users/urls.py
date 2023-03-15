from django.urls import path

from .views import SignUpView, profile, follow_user, unfollow_user, edit_profile, create_comment, upvote_post
from allauth.account.views import PasswordChangeView

urlpatterns = [
    path("<int:id>", profile, name='profile'),
    path('follow/<int:id>/', follow_user, name='follow_user'),
    path('unfollow/<int:id>/', unfollow_user, name='unfollow_user'),
    path('edit', edit_profile, name='edit-profile'),
    path('password-change', PasswordChangeView.as_view(), name='account_change_password1'),
    path('comment/', create_comment, name='create_comment'),
    path('upvote/', upvote_post, name='upvote_post')
]