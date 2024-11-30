from tdl.models import ItemList
from tdl.form import ItemForm, UpdateForm
from utils.pagination import make_pagination
import os
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

PER_PAGE = int(os.environ.get('PER_PAGE', 2))


class ListViewBase(ListView):
    template_name = 'tdl/pages/home.html'
    model = ItemList
    context_object_name = 'information'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                user=self.request.user
            ).order_by('-id')
        else:
            queryset = queryset.none()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('information'),
            PER_PAGE
        )

        context.update({
            'information': page_obj,
            'pagination_range': pagination_range,
            'title': 'Home',
            'user': self.request.user
        })

        return context


class ListViewHome(ListViewBase):
    template_name = 'tdl/pages/home.html'


class ListViewSearch(ListViewBase):
    template_name = 'tdl/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        queryset = queryset.filter(
            Q(name__icontains=search_term)
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context.update({
            'title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = 'authors:author_register'
    model = ItemList
    form_class = ItemForm
    success_url = reverse_lazy('tdl:home')
    template_name = 'tdl/partials/task_page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['msg'] = 'Create'

        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'authors:author_register'
    model = ItemList
    form_class = UpdateForm
    success_url = reverse_lazy('tdl:home')
    template_name = 'tdl/partials/task_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['msg'] = 'Update'
        context['completed'] = self.object.completed

        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'authors:author_register'
    model = ItemList
    context_object_name = 'item'
    success_url = reverse_lazy('tdl:home')


class DetailViewItemVisualization(LoginRequiredMixin, DetailView):
    login_url = 'authors:author_register'
    template_name = 'tdl/partials/task_view.html'
    model = ItemList
    context_object_name = 'item'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            pk=self.kwargs.get('pk'),
            user=self.request.user)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Item visualization',
            'item': context.get('item'),
        })

        return context
