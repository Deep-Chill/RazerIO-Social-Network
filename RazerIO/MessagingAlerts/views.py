from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    # conversations = Membership.objects.filter(user=request.user)
    # context = {'conversations':conversations}
    return render(request, 'messages.html')
