from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, EditUserForm


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form.add_error('username', 'نام کاربری با کلمه عبور مطابقت ندارد')
    context = {'page': 'login', 'form': form}
    return render(request, 'myaccounts/login-register.html', context)


def registerPage(request):
    rform = RegisterForm(request.POST or None)
    if rform.is_valid():
        username = rform.cleaned_data.get('username')
        email = rform.cleaned_data.get('email')
        password = rform.cleaned_data.get('password')
        user = User.objects.create_user(username, email, password)
        login(request, user)
        return redirect('home')
    context = {'page': 'register', 'form': rform}
    return render(request, 'myaccounts/login-register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profilePage(request):
    context = {}
    return render(request, 'myaccounts/profile.html', context)


@login_required(login_url='login')
def editProfile(request,):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user is None:
        raise Http404()
    editForm = EditUserForm(request.POST or None, initial={'email': user.email,
                                                           'first_name': user.first_name,
                                                           'last_name': user.last_name})

    if editForm.is_valid():
        first_name = editForm.cleaned_data.get('first_name')
        last_Name = editForm.cleaned_data.get('last_name')
        email = editForm.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_Name
        user.email = email
        user.save()
        return redirect('profile')

    context = {'editForm': editForm}
    return render(request, 'myaccounts/edit_profile.html', context)


def profile_menu(request):
    return render(request, 'myaccounts/sidebar.html')
