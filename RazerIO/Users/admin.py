from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UserFollowing, Skill, User_Skill


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "Bio", "Salary", "Country"]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'Bio', 'Salary', 'Company', 'Country', 'Region', 'ProfilePic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'Bio', 'Salary', 'Company',
                     'Country', 'Region')
    ordering = ('username',)


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFollowing)
admin.site.register(Skill)
admin.site.register(User_Skill)