from django import template

register = template.Library()

@register.filter
def filter_comments(comments, post):
    return comments.filter(Post=post)

@register.filter
def filter_upvotes(upvotes, post):
    return upvotes.filter(Post=post)

@register.filter
def has_upvoted(post, user):
    return post.upvote_set.filter(User=user).exists()
