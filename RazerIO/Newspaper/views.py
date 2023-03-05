from django.shortcuts import render
from .models import Newspaper as Nsp
from .models import Article, Article_Comment
from django.shortcuts import get_object_or_404
from .forms import ArticleForm, ArticleCommentForm
from .models import Newspaper, Article

# Create your views here.

def newspaper_view(request, id):
    user = request.user
    newspaper = Nsp.objects.get(Owner=id)
    id = newspaper.id
    articles = Article.objects.filter(Newspaper_id=id)
    context = {"newspaper": newspaper, "id":id, "articles":articles}
    return render(request, 'newspaper.html', context=context)


def ArticleView(request, id):
    article = get_object_or_404(Article, id=id)
    author = Nsp.objects.get(id=article.Newspaper.id).Owner

    if request.method == 'POST':
        form = ArticleCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if form.cleaned_data['Is_Anonymous']:
                comment.Text = form.cleaned_data['Text']
                comment.Author = None
                if form.cleaned_data['Show_Company']:
                    comment.Company = request.user.Company
                else:
                    comment.Company = None
            else:
                comment.Text = form.cleaned_data['Text']
                comment.Author = request.user
                comment.Company = request.user.Company
            comment.Article = article
            comment.save()
            # Redirect to the same page to see the comment added
            return redirect('article', id=id)
    else:
        form = ArticleCommentForm()

    comments = Article_Comment.objects.filter(Article=article)

    context = {
        'Article': article,
        'author': author,
        'form': form,
        'comments': comments,
    }
    return render(request, 'article.html', context=context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



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

def Add_Comment(request, id):
    article = get_object_or_404(Article, id=id)
    comment = None

    if request.method == "POST":
        form = ArticleCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if form.cleaned_data['Is_Anonymous']:
                comment.Text = form.cleaned_data['Text']
                comment.Author = None
                if form.cleaned_data['Show_Company']:
                    comment.Company = request.user.Company
                else:
                    comment.Company = None
            else:
                comment.Text = form.cleaned_data['Text']
                comment.Author = request.user
                comment.Company = request.user.Company
            comment.Article = article
            comment.save()
    else:
        form = ArticleCommentForm()

    context = {'form':form, 'comment':comment, 'article':article}
    return render(request, 'create_comment.html', context)
