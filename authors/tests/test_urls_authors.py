from django.test import TestCase
from django.urls import reverse, resolve
from authors import views


class TestUrlsAuthors(TestCase):
    def test_url_register_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_url_register_has_the_correct_view(self):
        url = resolve(reverse('authors:register'))
        self.assertEqual(url.func, views.register)

    def test_url_register_returns_status_code_200(self):
        url = self.client.get(reverse('authors:register'))
        self.assertEqual(url.status_code, 200)

    def test_url_register_returns_correct_template(self):
        url = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(url, 'authors/pages/register.html')
