from django.test import TestCase
from django.urls import reverse, resolve
from tdl import views


class TestURlTDLHome(TestCase):
    def test_url_home_is_correct(self):
        url = reverse('tdl:home')
        self.assertEqual(url, '/')

    def test_url_home_has_the_correct_view(self):
        url = resolve(reverse('tdl:home'))
        self.assertEqual(url.func, views.home)

    def test_url_home_returns_status_code_200(self):
        url = self.client.get(reverse('tdl:home'))
        self.assertEqual(url.status_code, 200)

    def test_url_home_returns_correct_template(self):
        url = self.client.get(reverse('tdl:home'))
        self.assertTemplateUsed(url, 'tdl/pages/home.html')
