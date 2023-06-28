from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import logout
from .models import *
from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime
import os
from .settings import BASE_DIR

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'google-credentials.json')

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
            draft = request.POST.get('draft')
            if draft=="Draft":
                is_visible = False
            else:
                is_visible = True
            blog = Blog(title=title,image=image,summary=summary,content=content, author=request.user, is_visible=is_visible)
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
            author_blogs = Blog.objects.filter(author__id=user.id)
            categories = Category.objects.all()
            doctors = []
            profiles = Profile.objects.all()
            for prof in profiles:
                if prof.is_doctor:
                    doctors.append(prof)
            if profile.is_doctor:
                doctor = True
                appointments = Appointment.objects.filter(doctor__id = request.user.id)
            else:
                doctor = False
                appointments = Appointment.objects.filter(patient__user__id=request.user.id)
            return render(request, 'dashboard.html', {'doctor':doctor,'doctors':doctors, 'blogs':blogs, 'categories':categories, 'author_blogs':author_blogs, 'appointments':appointments})
    else:
        return redirect('login_form')
    
def upload(request, id):
    blog = Blog.objects.get(id=id)
    blog.is_visible = True
    blog.save()
    return redirect('dashboard')
    
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

def apply(request, id):
    if request.method=='POST':
        print(request.user)
        speciality = request.POST.get('speciality')
        datet = request.POST.get('datetime')
        date = datetime.datetime.strptime(datet, '%Y-%m-%dT%H:%M').date()
        time = datetime.datetime.strptime(datet, '%Y-%m-%dT%H:%M').time()
        new = datetime.datetime.strptime(datet, '%Y-%m-%dT%H:%M') + datetime.timedelta(minutes=45)
        print(date)
        print(time)
        end_time = new.time()
        print(end_time)
        doctor_user = Profile.objects.get(id=id).user
        patient_profile = Profile.objects.get(user__id=request.user.id)
        appointment = Appointment(speciality=speciality, doctor=doctor_user, patient=patient_profile, is_pending=True,start_time=time, end_time=end_time, date=date)
        appointment.save()
        return redirect('dashboard')
    else:
        doctor_profile = Profile.objects.get(user__id=id)
        return render(request, 'form.html', {'doctor_profile':doctor_profile})

def approve(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.is_pending = False
    appointment.save()
    return redirect('dashboard')

def test_calendar(request):
    print("RUNNING TEST_CALENDAR()")

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    print(credentials)
    print(service)
    # CREATE A NEW EVENT
    new_event = {
    'summary': "Ben Hammond Tech's Super Awesome Event",
    'location': 'Denver, CO USA',
    'description': 'https://benhammond.tech',
    'start': {
        'date': f"{datetime.date.today()}",
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'date': f"{datetime.date.today() + datetime.timedelta(days=3)}",
        'timeZone': 'Asia/Kolkata',
    },
    }
    print(new_event)
    print(CAL_ID)
    service.events().insert(calendarId=CAL_ID, body=new_event).execute()
    print('Event created')

 # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # LOG THEM ALL OUT IN DEV TOOLS CONSOLE
    for e in events:

        print(e)

    #uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
        # service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()

    
    return events