from datetime import timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.template.loader import render_to_string
from .forms import CustomUserCreationForm, NewPost, CustomUserChangeForm
from Company.models import Company
from Feed.models import Post, Comment, Upvote
from Newspaper.models import Article, Newspaper as Nsp
from Users.models import CustomUser, UserFollowing, Education
from Endorsements.models import Endorsement
from Projects.models import Experience
from allauth.account.models import EmailAddress
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

User = settings.AUTH_USER_MODEL
past_48_hours = timezone.now() - timedelta(hours=48)


from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


user_weights = {
    'company_ratings': 0.20,
    'university_ratings': 0.15,
    'current_company_rating': 0.10,
    'position_score': 0.10,
    'certifications_score': 0.05,
    'industry_participation_score': 0.05,
    'awards_score': 0.05,
    'reputation_score': 0.10,
    'community_engagement_score': 0.05,
    'technical_skills_score': 0.05,
    'open_source_contributions_score': 0.03,
    'patents_score': 0.03,
    'publications_score': 0.02,
    'industry_experience_score': 0.02,
    'professional_network_strength_score': 0.02,
}
def get_user_score(user):
    company_ratings_score = ...
    university_ratings_score = ...
    current_company_rating_score = ...
    position_score = ...
    certifications_score = ...
    industry_participation_score = ...
    awards_score = ...
    reputation_score = ...
    community_engagement_score = ...
    technical_skills_score = ...
    open_source_contributions_score = ...
    patents_score = ...
    publications_score = ...
    industry_experience_score = ...
    professional_network_strength_score = ...

    user_score = (
        user_weights['company_ratings'] * company_ratings_score +
        user_weights['university_ratings'] * university_ratings_score +
        user_weights['current_company_rating'] * current_company_rating_score +
        user_weights['position_score'] * position_score +
        user_weights['certifications_score'] * certifications_score +
        user_weights['industry_participation_score'] * industry_participation_score +
        user_weights['awards_score'] * awards_score +
        user_weights['reputation_score'] * reputation_score +
        user_weights['community_engagement_score'] * community_engagement_score +
        user_weights['technical_skills_score'] * technical_skills_score +
        user_weights['open_source_contributions_score'] * open_source_contributions_score +
        user_weights['patents_score'] * patents_score +
        user_weights['publications_score'] * publications_score +
        user_weights['industry_experience_score'] * industry_experience_score +
        user_weights['professional_network_strength_score'] * professional_network_strength_score
    )

    return user_score


def profile(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        newspaper = Nsp.objects.get(Owner=id)
    except ObjectDoesNotExist:
        newspaper = None
    followers = UserFollowing.objects.filter(Following_User_ID=id)
    users_following = UserFollowing.objects.filter(User=id)
    endorsements = Endorsement.objects.filter(receiver=id)
    is_following = False
    education = Education.objects.filter(user=user)
    owned_experience = Experience.objects.filter(owner=user)
    collaborated_experience = Experience.objects.filter(collaborators__in=[user])
    experiences = owned_experience|collaborated_experience
    experiences = experiences.distinct().order_by('status')
    mutual_follow = False

    if request.user.is_authenticated:
        following = UserFollowing.objects.filter(User=request.user, Following_User_ID=user).exists()
        if following:
            is_following = True
        mutual_follow = UserFollowing.objects.filter(User=request.user, Following_User_ID=user).exists() and UserFollowing.objects.filter(User=user, Following_User_ID=request.user).exists()

    context = {
        "id": id,
        "newspaper": newspaper,
        "followers": followers,
        "following": users_following,
        "user1": user,
        "is_following": is_following,
        "endorsements":endorsements,
        "education":education,
        "owned_project":owned_experience,
        "collaborated_project":collaborated_experience,
        "experiences":experiences,
        "mutual_follow":mutual_follow
    }
    return render(request, 'profile.html', context=context)



def index(request):
    context = {}
    comments = Comment.objects.all()
    upvotes = Upvote.objects.all()
    if request.user.is_authenticated:
        user = request.user
        user_upvotes = Upvote.objects.filter(User=request.user)

        # Fetch all the necessary data with a few queries
        following_ids = UserFollowing.objects.filter(User=user).values_list('Following_User_ID', flat=True)
        friends_posts = Post.objects.filter(Q(Author__in=following_ids) | Q(Author=user), Category='Friends').select_related('Author').only('Author', 'Text', 'Date_Created')
        national_posts = Post.objects.filter(Category='National', Country=user.Country).select_related('Author').only('Author', 'Text', 'Date_Created')
        company_posts = Post.objects.filter(Category='Organization', Company=user.Company).select_related('Author').only('Author', 'Text', 'Date_Created')
        articles = Article.objects.filter(Date_Published__gte=timezone.now() - timezone.timedelta(hours=48)).annotate(num_upvotes=Count('articleupvote'))

        # Handle the POST request separately to avoid unnecessary database queries
        if request.method == "POST":
            form = NewPost(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.Author = user
                new_post.Text = form.cleaned_data['text']
                if new_post.Category == 'Organization':
                    new_post.Company = user.Company
                if new_post.Category == 'National':
                    new_post.Country = user.Country

                new_post.save()
                return JsonResponse({'status': 'ok', 'text': new_post.Text})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
        else:
            form = NewPost()

        # Pass all the data to the template context in a single dictionary
        context = {
            "FriendsPosts": friends_posts.order_by('-Date_Created'),
            "form": form,
            "Articles": articles.order_by('-num_upvotes', '-Date_Published'),
            "NationalPosts": national_posts.order_by('-Date_Created'),
            "CompanyPosts": company_posts.order_by('-Date_Created'),
            "comments":comments,
            "upvotes":upvotes,
            'user_upvotes': user_upvotes,
        }

    return render(request, 'home.html', context=context)

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

from allauth.account.forms import AddEmailForm

from allauth.account.forms import AddEmailForm
from django.shortcuts import render
from .forms import CustomUserChangeForm


def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        add_email_form = AddEmailForm(request.POST)
        if form.is_valid():
            edited_profile = form.save(commit=False)
            edited_profile.save()
            return redirect('profile', id=request.user.id)
    else:
        form = CustomUserChangeForm(instance=request.user)
        add_email_form = AddEmailForm()
    return render(request, 'edit_profile.html', {'form':form, 'add_email_form': add_email_form})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment_text')
        print('create_comment called with post_id:', post_id, 'comment_text:', comment_text)
        post = Post.objects.get(id=post_id)
        comment = Comment(Author=request.user, Post=post, Text=comment_text)
        comment.save()
        rendered_comment = render_to_string('comment.html', {'comment': comment})
        print(rendered_comment)
        return JsonResponse({'html': rendered_comment})

@csrf_exempt
def upvote_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        print('upvote_post called with post_id:', post_id)
        post = Post.objects.get(id=post_id)
        upvote, created = Upvote.objects.get_or_create(User=request.user, Post=post)
        if not created:
            upvote.delete()
        upvote_count = post.upvote_set.count()
        return JsonResponse({'upvote_count': upvote_count})

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing paths ...
    path('comment/', views.create_comment, name='create_comment'),
    path('upvote/', views.upvote_post, name='upvote_post'),
]
