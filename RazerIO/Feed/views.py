from django.shortcuts import render
from .models import Post
from django.http import JsonResponse


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.Author:
        post.delete()
        return JsonResponse({'post_id': post_id})
    else:
        return JsonResponse({'error': 'You are not authorized to delete this post'})

def delete_post_ajax(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.Author:
        post.delete()
        return JsonResponse({'post_id': post_id})
    else:
        return JsonResponse({'error': 'You are not authorized to delete this post'})
