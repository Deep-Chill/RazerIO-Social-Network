from django.urls import path

from .views import SignUpView, profile, follow_user, unfollow_user
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:id>", profile, name='profile'),
    path('follow/<int:id>/', follow_user, name='follow_user'),
    path('unfollow/<int:id>/', unfollow_user, name='unfollow_user'),

]