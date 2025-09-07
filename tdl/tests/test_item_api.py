from django.urls import reverse
from rest_framework.test import APITestCase

from utils.create_item import create_items, create_user


class ItemAPITest(APITestCase):
    def get_jwt_acess_token(self, user=None):
        if user is None:
            user = create_user()

        response = self.client.post(reverse(
            'tdl:token_obtain_pair'
        ),
            data={
                'username': user.username,
                'password': 'test'
            }
        )

        return response.data.get('access')

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

    def test_item_api_list_logged_user_can_create_a_item(self):
        data = {
            'name': 'test-name',
            'completed': False,
        }

        response = self.client.post(reverse(
            'tdl:item-api-list'
        ),
            data={**data},
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_acess_token()}'
        )

        self.assertEqual(response.status_code, 201)

    def test_item_api_list_logged_user_can_update_a_item(self):
        expected_name = 'name atualized'
        user = create_items(1)

        response = self.client.get(reverse(
            'tdl:item-api-list'
        ))
        result = response.data.get('results')[0]

        self.assertEqual(result['name'], 'item-0')

        self.client.patch(reverse(
            'tdl:item-api-detail', kwargs={'pk': 1}
        ),
            data={'name': expected_name},
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_acess_token(user=user)}'
        )

        response = self.client.get(reverse(
            'tdl:item-api-list'
        ))
        result = response.data.get('results')[0]

        self.assertEqual(result['name'], expected_name)

    def test_item_api_list_logged_user_cant_update_a_item_owned_by_another_user(self):  # noqa E501
        expected_name = 'name atualized'
        create_items(1)
        user = create_user(username='test2')

        response = self.client.get(reverse(
            'tdl:item-api-list'
        ))
        result = response.data.get('results')[0]

        self.assertEqual(result['name'], 'item-0')

        response = self.client.patch(reverse(
            'tdl:item-api-detail', kwargs={'pk': 1}
        ),
            data={'name': expected_name},
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_acess_token(user=user)}'
        )

        self.assertEqual(response.status_code, 403)
