from django.shortcuts import render
from .models import Endorsement

# Create your views here.

def endorsement(request):
    endorsements = Endorsement.objects.filter(receiver=request.user)
    context = {"endorsements":endorsements}
    return render(request, 'endorsements.html', context=context)