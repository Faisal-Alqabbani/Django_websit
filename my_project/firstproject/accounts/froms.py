from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.EmailInput())
    first_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput
    )
    last_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput
    )
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
class ImageUpdatedForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
