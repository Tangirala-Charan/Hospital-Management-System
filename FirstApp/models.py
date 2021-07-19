from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class MyUserManager():
    def create_user(self, username, name, password = None):
        if not username:
            raise ValueError('Username Not Entered')

        user = self.model(
            username=username,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password):
        user = self.create_user(
            username,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Register(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255)
    gender_choice = (('Male', 'male'), ('Female', 'female'), ('Other', 'other'))
    gender = models.CharField(max_length=6, choices=gender_choice)
    age = models.IntegerField()
    email = models.EmailField(max_length=30, unique=True)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

class Appointment(models.Model):
    username = models.CharField(max_length=30, default='Charan7520')
    patient_name = models.CharField(max_length=30)
    doctor_choice = (('Mr. Sriraj', 'Mr. Sriraj'), ('Ms. Lalitha', 'Ms. Lalitha'), ('Mr. Tarun', 'Mr. Tarun'), ('Mr. Aditya', 'Mr. Aditya'))
    doctor_name = models.CharField(max_length=15, choices=doctor_choice)
    timings_choice = (('10:00 A.M - 11:00 A.M', '10:00 A.M - 11:00 A.M'), ('11:00 A.M - 12:00 P.M', '11:00 A.M - 12:00 P.M'), ('2:00 P.M - 3:00 P.M', '2:00 P.M - 3:00 P.M'), ('4:00 P.M - 5:00 P.M', '4:00 P.M - 5:00 P.M'), ('5:00 P.M - 6:00 P.M', '5:00 P.M - 6:00 P.M'))
    timings = models.CharField(max_length = 30, choices = timings_choice)
    age = models.IntegerField()
    phone_number = models.CharField(max_length = 10)
    symptoms = models.CharField(max_length = 255)
    status = models.CharField(max_length = 20, default='Pending')
    reason = models.CharField(max_length = 255)

    def __str__(self):
        return self.patient_name

class ContactUs(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.name
