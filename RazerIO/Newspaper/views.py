from django.shortcuts import render
from .models import Newspaper as Nsp
from .models import Article
# Create your views here.

def newspaper_view(request, id):
    user = request.user
    newspaper = Nsp.objects.get(Owner=id)
    id = newspaper.id
    articles = Article.objects.filter(Newspaper_id=id)
    context = {"newspaper": newspaper, "id":id, "articles":articles}
    return render(request, 'newspaper.html', context=context)


def ArticleView(request, id):
    user = request.user
    article = Article.objects.get(id=id)
    author = Nsp.objects.get(id=article.Newspaper.id).Owner
    context2 = {"Article":article, "Author":author}
    return render(request, 'article.html', context=context2)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ArticleForm
from .models import Newspaper, Article


@login_required
def write_article(request):
    user = request.user
    newspaper = Newspaper.objects.get(id=user.Newspaper.id)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.Newspaper = newspaper
            article.save()
            return redirect('article', id=article.id)
    else:
        form = ArticleForm()

    context = {'form': form, 'newspaper': newspaper}
    return render(request, 'write_article.html', context)
