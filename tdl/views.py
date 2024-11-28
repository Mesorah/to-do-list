from django.shortcuts import render, redirect, get_object_or_404
from tdl.models import ItemList
from tdl.form import ItemForm, UpdateForm
from django.urls import reverse
from utils.pagination import make_pagination
import os
from django.http import Http404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
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


@method_decorator(
    login_required(login_url='authors:author_register', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class CreateTaskViewT(CreateView):
    model = ItemList
    form_class = ItemForm
    success_url = reverse_lazy('tdl:home')
    template_name = 'tdl/partials/task_page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['msg'] = 'Add'

        return context


@method_decorator(
    login_required(login_url='authors:author_register', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class CreateTaskView(View):
    def render_task(self, form):
        return render(self.request, 'tdl/partials/task_page.html', context={
            'title': 'Add',
            'url_action': reverse('tdl:add_task'),
            'msg': 'Add',
            'form': form,
        })

    def get(self, request):
        form = ItemForm()

        return self.render_task(form)

    def post(self, request):
        form = ItemForm(self.request.POST)

        if form.is_valid():
            completed = form.cleaned_data['completed']
            new_item = ItemList(name=form.cleaned_data['name'])
            new_item.user = self.request.user
            new_item.completed = completed
            new_item.save()
            return redirect('tdl:home')

        return self.render_task(form)


@method_decorator(
    login_required(login_url='authors:author_register', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class RemoveTaskView(View):
    def post(self, request, id):
        item = get_object_or_404(ItemList, pk=id, user=request.user)
        item.delete()
        messages.success(request, 'Tarefa removida com sucesso!')

        return redirect('tdl:home')


@method_decorator(
    login_required(login_url='authors:author_register', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class UpdateTaskView(View):
    def render_task(self, form, complet, id):
        return render(self.request, 'tdl/partials/task_page.html', context={
            'title': 'Edit',
            'url_action': reverse('tdl:update_task_page', args=[id]),
            'msg': 'Edit',
            'form': form,
            'completed': complet,
        })

    def get_item(self, id):
        item = get_object_or_404(ItemList, pk=id, user=self.request.user)
        return item

    def update_task(self, item, form):
        nome = form.cleaned_data['name']
        att_completed = form.cleaned_data['completed']

        if nome == '' and len(item.name) >= 1:
            nome = item.name
        else:
            item.name = nome

        item.completed = att_completed
        item.save()

    def get(self, response, id):
        item = self.get_item(id)

        form = UpdateForm(instance=item)

        return self.render_task(form, item.completed, id)

    def post(self, response, id):
        item = self.get_item(id)
        form = UpdateForm(self.request.POST, instance=item)

        old_name = item.name
        old_completed = item.completed

        if form.is_valid():

            self.update_task(item, form)
            print(item.name, old_name, item.completed, old_completed)

            if item.name != old_name or item.completed != old_completed:
                messages.success(
                    self.request,
                    'Tarefa atualizada com sucesso!'
                )
                return redirect('tdl:home')
            else:
                messages.warning(self.request, 'Nenhuma alteração detectada.')

        return self.render_task(form, item, id)


@method_decorator(
    login_required(login_url='authors:author_register', redirect_field_name='next'), # noqa E501
    name='dispatch'
)
class DetailViewItemVisualization(DetailView):
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
