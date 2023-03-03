from django.shortcuts import render
from Newspaper.models import Newspaper as Nsp
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from Feed.models import Post
from Company.models import Company
from Users.models import UserFollowing, CustomUser
from django.conf import settings
from .forms import NewPost
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

User = settings.AUTH_USER_MODEL


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


def index(request):
    if request.user.is_authenticated:
        user = request.user
        Following = UserFollowing.objects.filter(User=user).values('id')
        Posts = Post.objects.filter(Author__in=Following)
        if request.method == "POST":
            form = NewPost(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.Author = user
                new_post.Text = form.cleaned_data['text']
                new_post.save()
                return JsonResponse({'status': 'ok', 'text': new_post.Text})  # return a JSON response with the new post data
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})  # return a JSON response with the form errors
        else:
            form = NewPost()
        context = {"Posts": Posts, "form":form}
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
