from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def messages(request):
    return render(request, 'messages.html')
