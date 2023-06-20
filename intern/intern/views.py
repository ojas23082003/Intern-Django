from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import logout
from .models import *

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('login_form')
    
def dashboard(request, id):
    if request.user.is_authenticated:
        # user=User.objects.get(id=id)
        user = request.user
        profile = Profile.objects.filter(user__id=id)
        # print(profile.image)
        return render(request, 'dashboard.html',{'profile':profile, 'user':user})
    else:
        return redirect('login_form')
    
def logout_user(request):
    logout(request)
    return redirect('login_form')

def login_form(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        cnfpwd = request.POST.get('cnfpwd')

        if password==cnfpwd:
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                # print(user)
                id = user.id
                print(user.id)
                login(request, user=user)
                return redirect('dashboard', id=user.id)
            else:
                return render(request, 'login.html', {'message':"User not found"})
        else:
            return render(request, 'login.html', {'message':"Password doesn't match, please cross-check once."})
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
        prof = request.FILES.get('file')
        if passw==cnfpwd:
            user = User(username=username, first_name=fname, last_name=lname, email=email)
            user.set_password(passw)
            user.save()
            profile = Profile(address=address, usertype=type_user, image=prof, user=user)
            profile.save()
            return redirect('login_form')
        else:
            return render(request, 'signup.html', {'message':"Password doesn't match, please cross-check once."})
    else:
        return render(request, 'signup.html')