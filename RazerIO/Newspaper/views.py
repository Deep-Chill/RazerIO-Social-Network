from django.shortcuts import render
from .models import Newspaper as Nsp
from .models import Article
# Create your views here.

def Newspaper(request, id):
    user = request.user
    Newspaper = Nsp.objects.get(Owner=id)
    id = Newspaper.id
    Articles = Article.objects.filter(Newspaper_id=id)
    context = {"Newspaper": Newspaper, "id":id, "articles":Articles}
    return render(request, 'newspaper.html', context=context)

def ArticleView(request, id):
    user = request.user
    article = Article.objects.get(id=id)
    author = Nsp.objects.get(id=article.Newspaper.id).Owner
    context2 = {"Article":article, "Author":author}
    return render(request, 'article.html', context=context2)
