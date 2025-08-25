from django import forms
from django.core.exceptions import ValidationError

from tdl.models import ItemList
from tdl.validators import ItemValidator


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

    def clean(self):
        super_clean = super().clean()

        ItemValidator(data=super_clean, validation_error=ValidationError)

        return super_clean


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
