from django.urls import path

from .views import new_project, projects

urlpatterns = [
    path('', projects, name='projects'),
    path('new_project/', new_project, name='new_project')
]