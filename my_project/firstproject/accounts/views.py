from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .froms import SignUpForm, ProfileForm, ImageUpdatedForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created by {username}!')
                return redirect('index')
        else:
            form = SignUpForm()


    return render(request,'signup.html',{'form':form})

def validation_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

@login_required
def profiles(request):
    if request.method == 'POST':
        form1 = ProfileForm(request.POST, instance=request.user)
        form_p = ImageUpdatedForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if form1.is_valid() and form_p.is_valid():
            form1.save()
            form_p.save()
            messages.success(request, f'Account has been updated by {request.user.username} !')
            return redirect('my_account')
    else:
        form1 = ProfileForm(instance=request.user)
        form_p = ImageUpdatedForm(instance=request.user.profile)
    return render(request, 'my_account.html', {'form1': form1, 'form_p': form_p})
@login_required
def profile(request):
    return render(request, 'profile.html')


# Create your views here.
