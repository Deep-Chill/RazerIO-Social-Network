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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_nested_item(dictionary, keys):
    keys = keys.split('.')
    value = dictionary
    for key in keys:
        value = value.get(key)
    return value


@register.filter
def get_job_count(dictionary, category):
    return dictionary.get(category, 0)

@register.filter
def generate_alias(category_id):
    return 'category_' + ''.join(e for e in category_id if e.isalnum()) + '_count'
