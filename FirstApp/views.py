from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from .admin import *
from .backends import *
from Hospital_Management import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        data_db = ContactUs(name=name, email=email, message=message)
        data_db.save()
    return render(request, "contact.html")

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = AuthBackend().authenticate(request, username=username, password=password)
            if user:
                messages.success(request, "Logged in.")
                login(request, user)
                if not user.is_staff:
                    return redirect("home")
                else:
                    messages.info(request, "Invalid username or password")
                    return redirect("register")
            else:
                messages.info(request, "Invalid username or password")
                return redirect("register")
        return render(request, "login.html")
    else:
        return redirect("home")

def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = AuthBackend().authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect("details")
                else:
                    messages.info(request, "You don't have permission to login")
                    return redirect("home")
            else:
                messages.info(request, "You don't have permission to login")
                return redirect("home")
        return render(request, "signin.html")
    else:
        return redirect("home")

def signout(request):
    messages.info(request, "Logged out")
    logout(request)
    return redirect("home")

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserCreationForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, "Thanks for registering. Please enjoy the stay")
                data = Register.objects.get(username=form.cleaned_data['username'])
                data.save()
                new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, new_user)
                return redirect("home")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.info(request, field.title() + ": " + error)
        return render(request, "register.html")
    else:
        return redirect("home")

def appointment(request):
    if request.method == "POST":
        username = request.user.username
        patient_name = request.POST['patient_name']
        doctor_name = request.POST['doctor_name']
        age = request.POST['age']
        symptoms = request.POST['symptoms']
        timings = request.POST['timings']
        phone_number = request.POST['phone_number']

        user = Appointment(username=username, patient_name=patient_name, doctor_name=doctor_name, age=age, timings=timings, symptoms=symptoms, phone_number=phone)
        user.save()

        return redirect("Appointmentlist")
    return render(request, "appointment.html")

def appointmentlist(request):
    records = Appointment.objects.filter(username=request.user)
    return render(request, "appointmentlist.html", {'records': records})

def profile(request):
    if request.user.is_authenticated:
        data = request.user
        return render(request, "profile.html", {'data': data})

def update(request):
    if request.user.is_authenticated:
        data = request.user
        if request.method == "POST":
            data_db = Register.objects.get(id=data.id)
            data_db.name = request.POST['name']
            data_db.email = request.POST['email']
            data_db.phone_number = request.POST['phone_number']
            data_db.address = request.POST['address']
            data_db.age = request.POST['age']
            data_db.save()
            messages.success(request, "Your account has been updated successfully")
            return redirect("profile")
        return render(request, "update.html", {'data': data})

def details(request):
    if request.user.is_authenticated:
        data = Appointment.objects.all()
        return render(request, "details.html", {'data': data})
    else:
        return redirect("home")

def reason(request, Id):
    data = Appointment.objects.get(id=Id)
    data.status = "Cancelled"
    data.reason = request.POST['reason_text']
    print(data.reason)
    data.save()
    return redirect("details")

def accept(request, Id):
    data = Appointment.objects.get(id=Id)
    data.status = "Accepted"
    data.save()
    return redirect("details")
