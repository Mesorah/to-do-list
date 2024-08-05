from django.shortcuts import render, redirect, get_object_or_404
from tdl.models import ItemList
from tdl.form import ItemForm, UpdateForm
from django.urls import reverse
from utils.pagination import make_pagination
import os
from django.http import Http404
from django.db.models import Q


PER_PAGE = int(os.environ.get('PER_PAGE', 2))


def home(request):
    information = ItemList.objects.all().order_by('-id')

    page_obj, pagination_range = make_pagination(request, information, PER_PAGE) # noqa E501

    return render(request, 'tdl/pages/home.html', context={
        'information': page_obj,
        'pagination_range': pagination_range,
        'title': 'Home',
    })


def add_task_page(request):
    form = ItemForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Add',
        'url_action': reverse('tdl:add_task'),
        'msg': 'Add',
        'form': form,
    })


def add_task(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            completed = form.cleaned_data['completed']
            new_item = ItemList(name=form.cleaned_data['name'])
            if completed is not None:
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


def remove_task_page(request, id):
    item = get_object_or_404(ItemList, pk=id)
    item.delete()

    return redirect('tdl:home')


def update_task_page(request, id):
    item = get_object_or_404(ItemList, pk=id)

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['name']
            completed = form.cleaned_data['completed']
            print(completed)
            item.name = nome
            item.save()
            return redirect(reverse('tdl:home'))

    else:
        form = UpdateForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Update',
        'url_action': reverse('tdl:update_task_page', args=[id]),
        'msg': 'Edit',
        'form': form,
        'completed': completed
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


def item_visualization(request, id):
    item = get_object_or_404(ItemList, pk=id)

    return render(request, 'tdl/partials/task_view.html', context={
        'title': 'Item visualization',
        'item': item,
    })
