from django.contrib import admin
from .models import Newspaper, Article, Article_Comment
# Register your models here.

admin.site.register(Newspaper)
admin.site.register(Article)
admin.site.register(Article_Comment)