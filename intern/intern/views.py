from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *

def index(request):
    return render(request, 'index.html')

def login_form(request):
    if request.method=="POST":
        username = request.POST.get('username')
        
    else:
        return render(request, 'login.html')

def signup_form(request):
    if request.method=="POST":

        # user = User()
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('pwd')
        cnfpwd = request.POST.get('cnfpwd')
        address = request.POST.get('address')
        type_user = request.POST.get('type')
        prof = request.POST.get('file')
        if passw==cnfpwd:
            user = User(username=username, first_name=fname, last_name=lname, email=email)
            user.set_password(passw)
            user.save()
            profile = Profile(address=address, usertype=type_user, image=prof, user=user)
            profile.save()
            return redirect('login_form')
        else:
            return render(request, 'signup.html', {'message':"Pas