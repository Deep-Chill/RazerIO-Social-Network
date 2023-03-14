from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from Company.models import Company
from django.contrib.auth import get_user_model

# Create your models here.

ARTICLE_CATEGORIES = (('Technology & Programming', 'Technology & Programming'), ('Artificial Intelligence',
                    'Artificial Intelligence'), ('Business & Industry', 'Business & Industry'),
                       ('Opinion & Analysis', 'Opinion & Analysis'), ('General', 'General')
                      )

class Newspaper(models.Model):
    Title = models.CharField(max_length=256)
    Owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                 related_name='Newspaper')
    Date_Created = models.DateField(auto_created=True)
    Logo = models.ImageField(upload_to='Newspaper/Logos', null=True)

    def __str__(self):
        return f'{self.Title}'

class Article(models.Model):
    Title = models.CharField(max_length=256)
    Date_Published = models.DateTimeField(auto_now_add=True)
    Text = RichTextField()
    Newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    Upvotes = models.ManyToManyField(get_user_model(), through='ArticleUpvote', related_name='upvoted_articles')
    Category = models.CharField(choices=ARTICLE_CATEGORIES, blank=True, max_length=50)
    def __str__(self):
        return f'{self.Title}'

class Article_Comment(models.Model):
    Text = models.TextField(max_length=10000)
    Author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               null=True, blank=True)
    Date_Published = models.DateTimeField(auto_now_add=True)
    Article = models.ForeignKey(Article, on_delete=models.CASCADE, default=1)
    Is_Anonymous = models.BooleanField(default=False)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                null=True, blank=True)
    Show_Company = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.Author} posted in {self.Article}'

class ArticleUpvote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
