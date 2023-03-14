from django.shortcuts import render
from .models import Newspaper as Nsp
from .models import Article, Article_Comment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ArticleForm, ArticleCommentForm
from .models import Newspaper, Article, ArticleUpvote
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count
from django.views.decorators.http import require_POST
from django.utils import timezone
# Create your views here.

def newspaper_view(request, id):
    user = request.user
    newspaper = Nsp.objects.get(Owner=id)
    id = newspaper.id
    articles = Article.objects.filter(Newspaper_id=id)
    context = {"newspaper": newspaper, "id":id, "articles":articles}
    return render(request, 'newspaper.html', context=context)

@login_required
def ArticleView(request, id):
    article = get_object_or_404(Article, id=id)
    author = Nsp.objects.select_related('Owner').get(id=article.Newspaper.id).Owner
    user = request.user

    if request.method == 'POST':
        form = ArticleCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if form.cleaned_data['Is_Anonymous']:
                comment.Text = form.cleaned_data['Text']
                comment.Author = None
                if form.cleaned_data['Show_Company']:
                    comment.Company = user.Company
                else:
                    comment.Company = None
            else:
                comment.Text = form.cleaned_data['Text']
                comment.Author = user
                comment.Company = user.Company
            comment.Article = article
            comment.save()
            # Redirect to the same page to see the comment added
            return redirect('article', id=id)
    else:
        form = ArticleCommentForm()
    total_upvotes = article.Upvotes.annotate(num_upvotes=Count('upvoted_articles')).values_list('num_upvotes',
                                                                                                 flat=True).count() or 0
    comments = Article_Comment.objects.filter(Article=article)
    context = {
        'Article': article,
        'author': author,
        'form': form,
        'comments': comments,
        'upvotes':total_upvotes
    }

    if request.method == 'POST' and 'upvote_button' in request.POST:
        if user not in article.Upvotes.all():
            article.upvoters.add(user)
            article.upvotes = F('upvotes') + 1
            article.save(update_fields=['upvotes'])
        return redirect('article', id=id)

    return render(request, 'article.html', context=context)

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
            comment.Text = form.cleaned_data['Text']
            if form.cleaned_data['Is_Anonymous']:
                comment.Author = None
                if form.cleaned_data['Show_Company']:
                    comment.Company = request.user.Company
            else:
                comment.Author = request.user
                comment.Company = request.user.Company
            comment.Article = article
            comment.save()
    else:
        form = ArticleCommentForm()

    context = {'form': form, 'comment': comment, 'article': article}
    return render(request, 'create_comment.html', context)


@require_POST
def upvote_article(request, id):
    article = get_object_or_404(Article, id=id)
    user = request.user
    if user.is_authenticated:
        if user in article.Upvotes.all():
            article.Upvotes.remove(user)
        else:
            article.Upvotes.add(user)
        return redirect('article', id=id)
    else:
        return redirect('login')

def articles_page(request):
    articles = Article.objects.filter(Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'top_articles.html', context=context)

def tech_articles(request):
    articles = Article.objects.filter(Category='Technology & Programming', Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'tech_articles.html', context=context)

def ai_articles(request):
    articles = Article.objects.filter(Category='Artificial Intelligence', Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'ai_articles.html', context=context)

def business_articles(request):
    articles = Article.objects.filter(Category='Business & Industry', Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'business_articles.html', context=context)

def opinion_articles(request):
    articles = Article.objects.filter(Category='Opinion & Analysis', Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'opinion_articles.html', context=context)

def general_articles(request):
    articles = Article.objects.filter(Category='General', Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))
    context = {'articles':articles}
    return render(request, 'general_articles.html', context=context)
