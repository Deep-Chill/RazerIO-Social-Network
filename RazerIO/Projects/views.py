from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'new_project.html', {'form': form})
