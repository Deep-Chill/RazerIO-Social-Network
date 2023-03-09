from django.contrib import admin
from .models import Newspaper, Article, Article_Comment, ArticleUpvote
# Register your models here.

admin.site.register(Newspaper)
admin.site.register(Article)
admin.site.register(Article_Comment)
admin.site.register(ArticleUpvote)