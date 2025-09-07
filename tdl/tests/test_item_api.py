from django.urls import reverse
from rest_framework.test import APITestCase

from utils.create_item import create_items


class ItemAPITest(APITestCase):
    def test_item_api_list_returns_status_code_200(self):
        response = self.client.get(reverse('tdl:item-api-list'))

        self.assertEqual(response.status_code, 200)

    def test_item_api_list_loads_correct_number_of_items(self):
        create_items(7)

        response = self.client.get(
            reverse('tdl:item-api-list') + '?page=1'
        )

        self.assertEqual(len(response.data.get('results')), 5)

    def test_item_api_list_user_must_send_jwt_token_to_create_item(self):
        response = self.client.post(reverse(
            'tdl:item-api-list'
        ))

        self.assertEqual(response.status_code, 401)
