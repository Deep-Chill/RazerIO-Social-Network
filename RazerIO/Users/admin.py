from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UserFollowing


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "Bio", "Salary", "Company"]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFollowing)

