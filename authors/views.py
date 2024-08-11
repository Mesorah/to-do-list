from django.shortcuts import render, redirect
from authors.form import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, \
    login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required


def author_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Registrado com sucesso')
            return redirect('authors:author_login')
    else:
        form = RegisterForm()

    print(request.user)

    return render(request, 'authors/pages/authors_authenticate.html', context={
        'form': form,
        'url_action': reverse('authors:author_register'),
        'title': 'Register',
        'msg': 'Register',
        'user': request.user
    })


def author_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Logado com sucesso')
                return redirect('tdl:home')

            else:
                messages.error(request, 'username or password is incorrect')

    else:
        form = LoginForm()

    return render(request, 'authors/pages/authors_authenticate.html', context={
        'form': form,
        'url_action': reverse('authors:author_login'),
        'title': 'Login',
        'msg': 'Login',
    })


@login_required(login_url='authors:author_login', redirect_field_name='next')
def author_logout(request):
    auth_logout(request)
    messages.success(request, 'Deslogado com sucesso')

    return redirect('authors:author_register')
