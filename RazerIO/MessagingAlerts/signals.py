from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Alert
from django.contrib.auth import get_user_model
from Users.models import UserFollowing
from Newspaper.models import Article_Comment

User = get_user_model()

@receiver(post_save, sender=UserFollowing)
def create_follow_alert(sender, instance, created, **kwargs):
    if created:
        recipient = instance.Following_User_ID
        actor = instance.User
        verb = 'followed you'
        target = None
        if recipient != actor:
            Alert.objects.create(
                recipient=recipient,
                actor=actor,
                verb=verb,
                target=target
            )

@receiver(post_save, sender=Article_Comment)
def create_article_comment_alert(sender, instance, created, **kwargs):
    if created:
        if not instance.Is_Anonymous:
            recipient = instance.Article.Newspaper.Owner
            actor = instance.Author
            verb = 'commented on'
            target = instance.Article
            if recipient != actor and recipient != instance.Author:
                Alert.objects.create(
                    recipient=recipient,
                    actor=actor,
                    verb=verb,
                    target=target
                )
        else:
            recipient = instance.Article.Newspaper.Owner
            actor = User.objects.get(username='Anonymous')
            verb = 'commented on'
            target = instance.Article
            if recipient != actor and recipient != instance.Author:
                Alert.objects.create(
                    recipient=recipient,
                    actor=actor,
                    verb=verb,
                    target=target
                )
