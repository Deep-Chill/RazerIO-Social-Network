from django.urls import path

from .views import Newspaper, ArticleView

urlpatterns = [
    path("<int:id>", Newspaper, name='newspaper'),
    path("article/<int:id>", ArticleView, name='article')
]