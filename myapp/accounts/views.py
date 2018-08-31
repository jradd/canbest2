from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import UserLoginForm, UserRegisterForm

from django.shortcuts import render, redirect


def login_view(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        login(request, user)

        next_page = request.GET.get("next")

        if next_page:
            return redirect(next_page)

        return redirect(reverse('posts:list'))

    ctx = {
        'form': form,
        'label': 'login',
        'title': 'Login here'
    }
    return render(request, "accounts/login.html", ctx)


def register_view(request):
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        password = form.cleaned_data.get("password")
        username = form.cleaned_data.get("username")

        user.set_password(password)
        user.save()

        new_user = authenticate(username=username, password=password)
        login(request, new_user)

        return redirect(reverse('posts:list'))

    ctx = {
        'form': form,
        'label': 'Sign up',
        'title': 'Sign up here'
    }
    return render(request, "accounts/register.html", ctx)


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))
