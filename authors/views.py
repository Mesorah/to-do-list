from authors.form import RegisterForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class AuthorRegisterViewT(FormView):
    template_name = 'authors/pages/authors_authenticate.html'
    form_class = RegisterForm
    success_url = reverse_lazy('tdl:home')

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        return super().form_valid(form)


class AuthorLoginView(LoginView):
    template_name = 'authors/pages/authors_authenticate.html'
    success_url = reverse_lazy('tdl:home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Login',
            'msg': 'Login',
        })

        return context

    def get_success_url(self):
        return self.success_url


@method_decorator(
    login_required(login_url='authors:author_login', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class AuthorLogoutView(LogoutView):
    def get_redirect_url(self):
        return '/'
