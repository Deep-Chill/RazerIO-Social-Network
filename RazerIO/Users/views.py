from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, NewPost
from Company.models import Company
from Feed.models import Post
from Newspaper.models import Article, Newspaper as Nsp
from Users.models import CustomUser, UserFollowing

User = settings.AUTH_USER_MODEL
past_48_hours = timezone.now() - timedelta(hours=48)


from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def profile(request, id):
    user = CustomUser.objects.get(id=id)
    newspaper = Nsp.objects.filter(Owner=id).first()
    followers = UserFollowing.objects.filter(Following_User_ID=id)
    users_following = UserFollowing.objects.filter(User=id)
    is_following = False

    if request.user.is_authenticated:
        following = UserFollowing.objects.filter(User=request.user, Following_User_ID=user).exists()
        if following:
            is_following = True

    context = {
        "id": id,
        "newspaper": newspaper,
        "followers": followers,
        "following": users_following,
        "user1": user,
        "is_following": is_following,
    }
    return render(request, 'profile.html', context=context)


from django.db.models import Q
from django.utils import timezone


def index(request):
    if request.user.is_authenticated:
        user = request.user
        Following = UserFollowing.objects.filter(User=user).values_list('Following_User_ID', flat=True)
        FriendsPosts = Post.objects.filter(Q(Author__in=Following) | Q(Author=user), Category='Friends').select_related(
            'Author')
        NationalPosts = Post.objects.filter(Category='National', Author__Country=user.Country).select_related('Author')
        CompanyPosts = Post.objects.filter(Category='Organization', Author__Company=user.Company).select_related(
            'Author')
        Articles = Article.objects.filter(Date_Published__gte=timezone.now() - timezone.timedelta(hours=48))

        if request.method == "POST":
            form = NewPost(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.Author = user
                new_post.Text = form.cleaned_data['text']
                new_post.save()
                return JsonResponse({'status': 'ok', 'text': new_post.Text})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
        else:
            form = NewPost()
        context = {
            "FriendsPosts": FriendsPosts,
            "form": form,
            "Articles": Articles,
            "NationalPosts": NationalPosts,
            "CompanyPosts": CompanyPosts,
        }
        return render(request, 'home.html', context=context)
    else:
        return render(request, 'home.html')


from django.shortcuts import get_object_or_404

def follow_user(request, id):
    user_to_follow = get_object_or_404(get_user_model(), id=int(id))
    if request.user != user_to_follow and not request.user.following.filter(Following_User_ID=user_to_follow).exists():
        request.user.following.create(Following_User_ID=user_to_follow)
    return redirect('profile', id=id)

def unfollow_user(request, id):
    user_to_unfollow = get_object_or_404(get_user_model(), id=id)
    request.user.following.filter(Following_User_ID=user_to_unfollow).delete()
    return redirect('profile', id=id)

def search(request):
    query = request.GET.get('q')
    users = get_user_model().objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    articles = Article.objects.filter(Q(Title__icontains=query) | Q(Text__icontains=query))
    newspapers = Nsp.objects.filter(Title__icontains=query)
    posts = Post.objects.filter(Text__icontains=query)
    context = {'users': users, 'articles': articles, 'newspapers': newspapers, 'posts': posts, 'query': query}
    return render(request, 'search_results.html', context=context)