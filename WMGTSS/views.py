from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home(request):
    return render(request, 'home/homepage.html')

def logoutSuccess(request):
    return render(request, 'user_auth/logout_successful.html')
