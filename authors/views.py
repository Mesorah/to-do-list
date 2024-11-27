from django.shortcuts import render, redirect
from authors.form import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, \
    login as auth_login, \
    logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View


class AuthorBaseView(View):
    def render_task(self, form, url_action, title, msg):
        return render(self.request, 'authors/pages/authors_authenticate.html', context={ # noqa E501
            'form': form,
            'url_action': reverse(url_action),
            'title': title,
            'msg': msg,
            'user': self.request.user
        })


class AuthorRegisterView(AuthorBaseView):
    def render_register_page(self, form):
        return self.render_task(
            form,
            'authors:author_register',
            'Register',
            'Register'
        )

    def get(self, request):
        form = RegisterForm()

        return self.render_register_page(form)

    def post(self, request):
        form = RegisterForm(self.request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(self.request, 'Registrado com sucesso')
            return redirect('authors:author_login')

        return self.render_register_page(form)


class AuthorLoginView(AuthorBaseView):
    def render_login_page(self, form):
        return self.render_task(
            form,
            'authors:author_login',
            'Login',
            'Login'
        )

    def get(self, response):
        form = LoginForm()

        return self.render_login_page(form)

    def post(self, response):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                self.request,
                username=username,
                password=password
            )

            if user is not None:
                auth_login(self.request, user)
                messages.success(self.request, 'Logado com sucesso')
                return redirect('tdl:home')

            else:
                messages.error(
                    self.request,
                    'username or password is incorrect'
                )

        return self.render_login_page(form)


@method_decorator(
    login_required(login_url='authors:author_login', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class AuthorLogoutView(View):
    def post(self, response):
        auth_logout(self.request)
        messages.success(self.request, 'Deslogado com sucesso')

        return redirect('authors:author_register')
