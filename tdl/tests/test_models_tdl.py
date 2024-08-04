from django.test import TestCase
from tdl.models import Author, ItemList


class AuthorModelTest(TestCase):
    def test_author_name(self):
        self.author = Author.objects.create(name='Juninho')

        self.assertEqual(str(self.author), 'Juninho')


class ItemListModelTest(TestCase):
    def test_item_list_name(self):
        self.item_list = ItemList.objects.create(name='Juninho')

        self.assertEqual(str(self.item_list), 'Juninho')
