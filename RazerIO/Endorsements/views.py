from django.shortcuts import render
from .models import Endorsement
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def endorsement(request, id):
    user = User.objects.get(id=id)
    endorsements = Endorsement.objects.filter(receiver=user)
    context = {"endorsements":endorsements}
    return render(request, 'endorsements.html', context=context)