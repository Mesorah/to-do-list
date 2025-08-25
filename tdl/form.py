from django import forms

from tdl.models import ItemList


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemList
        fields = ['name', 'completed']

        labels = {
            'name': 'Name',
        }

        error_messages = {
            'name': {
                'required': 'Este campo é obrigatório.',
            }
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = ItemList
        fields = ['name', 'completed']
        labels = {
            'name': 'Nome do item',
            'completed': 'Concluído',
        }
        error_messages = {
            'name': {
                'required': 'Este campo é obrigatório.',
            }
        }
