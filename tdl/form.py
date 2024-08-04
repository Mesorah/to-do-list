from django import forms
from tdl.models import ItemList
# from django.core.exceptions import ValidationError


class ItemForm(forms.ModelForm):
    completed = forms.BooleanField(
        label='completed',
        required=False
    )

    class Meta:
        model = ItemList
        fields = ['name']

        labels = {
            'name': 'Name',
        }

        error_messages = {
            'name': {
                'required': 'Este campo é obrigatório.',
            }
        }


class UpdateForm(forms.Form):
    name = forms.CharField(
        label='Nome do item para atulizar'
    )
    new_name = forms.CharField(
        label='Novo nome'
    )
    completed = forms.BooleanField(
        label='completed',
        required=False
    )
