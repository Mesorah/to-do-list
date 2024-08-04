from django.shortcuts import render, redirect
from tdl.models import ItemList
from tdl.form import ItemForm, UpdateForm
from django.urls import reverse
from django.contrib import messages


def home(request):
    information = ItemList.objects.all().order_by('-id')
    return render(request, 'tdl/pages/home.html', context={
        'information': information,
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


def remove_task_page(request):
    form = ItemForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Remove',
        'url_action': reverse('tdl:remove_task'),
        'msg': 'Remove',
        'form': form,
    })


def remove_task(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item_to_delete = form.cleaned_data['name']
            try:
                item_to_delete = ItemList.objects.get(name=item_to_delete)
                item_to_delete.delete()
            except ItemList.DoesNotExist:
                messages.error(request, 'Item não encontrado.')
                return redirect('tdl:remove_task')

            return redirect('tdl:home')
    else:
        form = ItemForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Remove',
        'url_action': reverse('tdl:remove_task'),
        'msg': 'Remove',
        'form': form,
    })


def update_task_page(request):
    form = UpdateForm()

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Update',
        'url_action': reverse('tdl:update_task'),
        'msg': 'Update',
        'form': form,
    })


def update_task(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['name']
            item_updated = form.cleaned_data['new_name']
            completed = form.cleaned_data['completed']
            try:
                item = ItemList.objects.get(name=item)
                item.name = item_updated
                if completed is not None:
                    item.completed = completed
                item.save()

            except ItemList.DoesNotExist:
                messages.error(request, 'Item não encontrado.')
                return redirect('tdl:update_task')

            return redirect('tdl:home')
    else:
        form = UpdateForm()

    if completed:
        checked = 'checked'

    return render(request, 'tdl/partials/task_page.html', context={
        'title': 'Update',
        'url_action': reverse('tdl:update_task'),
        'msg': 'Edit',
        'form': form,
        'checked': checked
    })
