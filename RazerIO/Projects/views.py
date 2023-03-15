from django.shortcuts import render, redirect, get_object_or_404
from .models import Experience
from .forms import ProjectForm, ProjectApplicationForm
from Users.models import Skill
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def projects(request):
    projects = Experience.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # save many-to-many fields after saving project
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'new_project.html', {'form': form})


def project(request, id):
    project = Experience.objects.get(id=id)
    context = {'project':project}
    return render(request, 'project.html', context=context)


@login_required
def apply_to_project(request, id):
    project = get_object_or_404(Experience, id=id)
    if request.method == 'POST':
        form = ProjectApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.user = request.user
            application.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect('project', id=project.id)
    else:
        form = ProjectApplicationForm()
    return render(request, 'apply_to_project.html', {'project': project, 'form': form})
