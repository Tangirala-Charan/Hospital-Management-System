from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    name = forms.CharField(label='Name', widget=forms.TextInput)
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    _password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'rows': 3}))
    CHOICES = [('Male', 'male'), ('Female', 'female'), ('Other', 'other')]
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    age = forms.IntegerField(label='Age', widget=forms.NumberInput)
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput)

    class Meta:
        model = Register
        fields = ('name','username','email','address','gender','age','phone')

    def clean_passwords(self):
        password = self.cleaned_data.get('password')
        _password = self.cleaned_data.get('_password')
        if password and _password and password != _password:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return _password
    
    def _post_clean(self):
        super()._post_clean()
        Password = self.cleaned_data.get('_password')
        if Password:
            try:
                password_validation.validate_password(Password, self.instance)
            except ValidationError as error:
                self.add_error('_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
