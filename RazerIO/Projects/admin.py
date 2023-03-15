from django.contrib import admin
from .models import ProjectApplication, ProjectComment, ProjectUpdate, Experience
# Register your models here.

admin.site.register(ProjectApplication)
admin.site.register(ProjectComment)
admin.site.register(ProjectUpdate)
admin.site.register(Experience)