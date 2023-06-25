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
    
def dashboard(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            title = request.POST.get('title')
            image = request.FILES.get('image')
            category = request.POST.get('category').lower()
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            categories = Category.objects.all()
            blog = Blog(title=title,image=image,summary=summary,content=content)
            blog.save()
            if categories!=None:
                for cate in categories:
                    if category==cate.name:
                        blog.category=cate
                        blog.save()
                        return redirect('dashboard')
            cat = Category(name=category)
            cat.save()
            blog.category=cat
            blog.save()
            return redirect('dashboard')
        else:
            user = request.user
            profile = Profile.objects.get(user__id=user.id)
            blogs = Blog.objects.all()
            categories = Category.objects.all()
            if profile.is_doctor:
                doctor = True
            else:
                doctor = False
            return render(request, 'dashboard.html', {'doctor':doctor, 'blogs':blogs, 'categories':categories})
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
                return redirect('dashboard')
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
            if type_user=="Doctor":
                doctor = True
            else:
                doctor = False
            profile = Profile(address=address, image=prof, user=user, is_doctor = doctor)
            profile.save()
            return redirect('login_form')
        else:
            return render(request, 'signup.html', {'message':"Password doesn't match, please cross-check once."})
    else:
        return render(request, 'signup.html')