from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import SignInForm, SignUpForm, EditProfileForm, ResetPasswordForm, ProfilePicForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.urls import reverse

@login_required(login_url='http:/127.0.0.1:8000/')
def add_to_favorites(request, food_id):
    if request.method == 'POST':
        food = Food.objects.get(pk=food_id)
        profile = request.user.profile
        profile.favorites.add(food)
        profile.save()
    return redirect(reverse('users:profile', args=[request.user.id]))


@login_required(login_url='http:/127.0.0.1:8000/')
def profile(request):
    try:
        user_profile = request.user.profile
        profile_pic = user_profile.profile_pic.url if user_profile.profile_pic else None
        return render(request, 'food_detail.html', {'user_profile': user_profile, 'profile_pic': profile_pic})
    except Profile.DoesNotExist:
        return render(request, 'food_detail.html', {})

@login_required(login_url='http://127.0.0.1:8000/')
def profile(request):
    try:
        user_profile = request.user.profile
        profile_pic = user_profile.profile_pic.url if user_profile.profile_pic else None
        return render(request, 'profile.html', {'user_profile': user_profile, 'profile_pic': profile_pic})
    except Profile.DoesNotExist:
        return render(request, 'profile.html', {})



@login_required(login_url='http:/127.0.0.1:8000/')
def edit_profile_pic(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfilePicForm(instance=request.user.profile)
    return render(request, 'edit_profile_pic.html', {'form': form})

@login_required(login_url='http://127.0.0.1:8000/')
def edit_profile_pic(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfilePicForm(instance=profile)
    return render(request, 'edit_profile_pic.html', {'form': form})


def sign_up(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('kafe:foods')
    return render(request, 'sign_up.html', {
        'form': form
    })


def sign_in(request):
    form = SignInForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('kafe:foods')
    return render(request, 'sign_in.html', {'form': form})

@login_required(login_url='http://127.0.0.1:8000/')
def sign_out(request):
    logout(request)
    return redirect('users:sign_in')

@login_required(login_url='http://127.0.0.1:8000/')
def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('kafe:foods')
    return render(request, 'edit_profile.html', {'form': form})

@login_required(login_url='http:/127.0.0.1:8000/')
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.user, data=request.POST)  
        if form.is_valid():
            user = form.save(request=request)
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль был успешно изменен.')  
            return redirect('users:sign_in')
    else:
        form = ResetPasswordForm(request.user) 
    return render(request, 'reset_password.html', {'form': form})