from django.contrib import admin
from .models import Project, ProjectApplication, ProjectComment, ProjectUpdate
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectApplication)
admin.site.register(ProjectComment)
admin.site.register(ProjectUpdate)
