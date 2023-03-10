from django import forms
from .models import Project, ProjectApplication
from django.core.validators import MaxValueValidator, MinValueValidator

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'looking_for_x_collaborators',
                  'collaborator_requirements', 'required_skills', 'location',
                  'benefits']
        labels = {
            'title': 'Title:',
            'description': 'Description:',
            'looking_for_x_collaborators': 'Number of collaborators needed:',
            'collaborator_requirements': 'Collaborator requirements:',
            'required_skills': 'Required skills:',
            'location': 'Location:',
            'benefits': 'Benefits:'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'rows':1}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows':5}),
            'looking_for_x_collaborators': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'collaborator_requirements': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows':5}),
            'required_skills': forms.SelectMultiple(attrs={'class': 'form-control form-control-sm'}),
            'location': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows':5}),
        }
        validators = [
            MaxValueValidator(10, message='Maximum value is 10.'),
            MinValueValidator(1, message='Minimum value is 1.'),
        ]



# Make all the fields above required in the form.

class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        model = ProjectApplication
        fields = ['message']
