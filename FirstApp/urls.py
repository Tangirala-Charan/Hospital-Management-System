from django.urls import path
from FirstApp import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.signin, name="login"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('register/', views.register, name="register"),
    path('logout/', views.signout, name="logout"),
    path('appointment/', views.appointment, name="appointment"),
    path('appointmentlist/', views.appointmentlist, name="appointmentlist"),
    path('profile/', views.profile, name="profile"),
    path('update/', views.update, name="update"),
    path('details/', views.details, name="details"),
    path('accept/<int:Id>', views.accept, name="accept"),
    path('reason/<int:Id>', views.reason, name="reason"),
]
