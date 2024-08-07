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


class UpdateForm(forms.Form):
    name = forms.CharField(
        label='Nome do item para atualizar',
        required=False
    )

    completed = forms.BooleanField(
        label='completed',
        required=False,
        initial=None
    )
