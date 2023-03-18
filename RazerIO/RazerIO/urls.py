"""RazerIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from Users.views import index, search
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LogoutView, LoginView, SignupView
from Newspaper.views import articles_page


urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path("profile/", include("Users.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("newspaper/", include("Newspaper.urls")),
    path("company/", include("Company.urls")),
    path("market/", include("Jobs.urls")),
    path('search/', search, name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include("MessagingAlerts.urls")),
    path('endorsements/', include("Endorsements.urls")),
    path('projects/', include("Projects.urls")),
    path('accounts/', include("allauth.urls")),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('news', articles_page, name='articles_page'),
    path('', include('Feed.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
