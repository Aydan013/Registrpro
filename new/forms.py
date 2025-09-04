from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomerUser

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomerUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')