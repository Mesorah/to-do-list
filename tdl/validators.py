from .models import ItemList


class ItemValidator:
    def __init__(self, data, validation_error):
        self.data = data
        self.validation_error = validation_error

        self.clean()

    def clean(self):
        self.clean_name()

    def clean_name(self):
        name = self.data.get('name')

        if ItemList.objects.filter(name=name).exists():
            raise self.validation_error('este nome já existe')

        return name
