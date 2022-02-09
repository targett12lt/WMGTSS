from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    '''Checks the user group of user and directs to the relevant homepage'''
    group = request.user.groups.filter(user=request.user)[0]
    if group.name=="Tutors":
        return render(request, 'home/homepage_tutor.html')
    else:
        return render(request, 'home/homepage.html')

def logoutSuccess(request):
    return render(request, 'user_auth/logout_successful.html')
