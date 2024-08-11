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


PER_PAGE = int(os.environ.get('PER_PAGE', 2))


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def home(request):
    information = ItemList.objects.filter(user=request.user).order_by('-id')

    page_obj, pagination_range = make_pagination(request, information, PER_PAGE) # noqa E501

    return render(request, 'tdl/pages/home.html', context={
        'information': page_obj,
        'pagination_range': pagination_range,
        'title': 'Home',
        'user': request.user
    })


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def add_task_page(request):
    form = ItemForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Add',
        'url_action': reverse('tdl:add_task'),
        'msg': 'Add',
        'form': form,
    })


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def add_task(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            completed = form.cleaned_data['completed']
            new_item = ItemList(name=form.cleaned_data['name'])
            new_item.user = request.user
            new_item.completed = completed
            new_item.save()
            return redirect('tdl:home')
    else:
        form = ItemForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Add',
        'url_action': reverse('tdl:add_task'),
        'msg': 'Add',
        'form': form,
    })


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def remove_task_page(request, id):
    item = get_object_or_404(ItemList, pk=id, user=request.user)
    item.delete()
    messages.success(request, 'Tarefa removida com sucesso!')

    return redirect('tdl:home')


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def update_task(request, id):
    form = UpdateForm(request.POST) # noqa F841

    return redirect('tdl:update_task_page', id=id)


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def update_task_page(request, id):
    item = get_object_or_404(ItemList, pk=id, user=request.user)
    complet = item.completed

    item_before_update = get_object_or_404(ItemList, pk=id, user=request.user)
    complet_before_update = item_before_update.completed

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=item)
        if form.is_valid():
            nome = form.cleaned_data['name']
            if nome == '' and len(item.name) >= 1:
                nome = item.name
            else:
                item.name = nome

            att_completed = form.cleaned_data['completed']
            item.completed = complet
            item.completed = att_completed
            item.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')

            if item.name != item_before_update.name or item.completed != complet_before_update: # noqa E501
                return redirect('tdl:home')
            else:
                messages.warning(request, 'Houve um erro ao atualizar a tarefa.') # noqa E501

    else:
        form = UpdateForm(instance=item)

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Edit',
        'url_action': reverse('tdl:update_task_page', args=[id]),
        'msg': 'Edit',
        'form': form,
        'completed': complet,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    information = ItemList.objects.filter(
        Q(name__icontains=search_term),
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, information, PER_PAGE) # noqa E501

    return render(request, 'tdl/pages/search.html', context={
        'title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'information': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })


@login_required(login_url='authors:author_register', redirect_field_name='next') # noqa E501
def item_visualization(request, id):
    item = get_object_or_404(ItemList, pk=id, user=request.user)

    return render(request, 'tdl/partials/task_view.html', context={
        'title': 'Item visualization',
        'item': item,
    })
