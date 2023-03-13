from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from Feed.models import Post
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "Bio", "Salary", "Company")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("Bio", "Salary", "Company")



class NewPost(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), label='Text')
    class Meta:
        model = Post
        fields = ['text', 'Category']


