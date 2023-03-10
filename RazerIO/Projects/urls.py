from django.urls import path

from .views import new_project, projects, project, apply_to_project

urlpatterns = [
    path('', projects, name='projects'),
    path('new_project/', new_project, name='new_project'),
    path('<int:id>/', project, name='project'),
    path('<int:id>/apply/', apply_to_project, name='apply_to_project')
]