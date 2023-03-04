from django.urls import path

from .views import newspaper_view, ArticleView, write_article

urlpatterns = [
    path("<int:id>", newspaper_view, name='newspaper'),
    path("article/<int:id>", ArticleView, name='article'),
    path('write_article/', write_article, name='write_article'),
]