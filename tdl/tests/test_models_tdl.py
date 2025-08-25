from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from tdl.form import ItemForm
from tdl.models import ItemList

# class AuthorModelTest(TestCase):
#     def test_author_name(self):
#         self.author = Author.objects.create(name='Juninho')

#         self.assertEqual(str(self.author), 'Juninho')


class ItemListModelTest(TestCase):
    def test_item_list_name(self):
        self.item_list = ItemList.objects.create(name='Juninho')

        self.assertEqual(str(self.item_list), 'Juninho')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.item = ItemList.objects.create(name='Test Task')

    def test_home_view(self):
        response = self.client.get(reverse('tdl:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/pages/home.html')
        self.assertContains(response, 'Test Task')

    def test_add_task_page_view(self):
        response = self.client.get(reverse('tdl:add_task_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/partials/task_page.html')

    def test_add_task(self):
        response = self.client.post(
            reverse('tdl:add_task_page'),
            {'name': 'New Task', 'completed': False})
        self.assertEqual(response.status_code, 302)  # Redirects after POST
        self.assertTrue(ItemList.objects.filter(name='New Task').exists())

    def test_remove_task_page_view(self):
        response = self.client.post(
            reverse('tdl:remove_task_page',
                    args=[self.item.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after POST
        self.assertFalse(ItemList.objects.filter(id=self.item.id).exists())

    def test_update_task_page_view(self):
        response = self.client.get(reverse('tdl:update_task_page',
                                           args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/partials/task_page.html')

    def test_update_task(self):
        response = self.client.post(reverse(
            'tdl:update_task_page', args=[self.item.id]),
            {'name': 'Updated Task'})
        self.assertEqual(response.status_code, 302)  # Redirects after POST
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Task')

    def test_search(self):
        response = self.client.get(reverse('tdl:search') + '?q=Test 1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_item_visualization(self):
        response = self.client.get(
            reverse('tdl:visualization',
                    args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/partials/task_view.html')
        self.assertContains(response, 'Test Task')


class AddTaskViewTest(TestCase):
    def test_add_task_valid_data(self):
        # Dados válidos para o formulário
        form_data = {
            'name': 'Test Task',
            'completed': True  # ou False, se preferir
        }

        # Envia uma requisição POST com os dados do formulário
        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        # Verifica se o item foi realmente criado
        self.assertEqual(ItemList.objects.count(), 1)
        new_item = ItemList.objects.first()
        self.assertEqual(new_item.name, 'Test Task')
        self.assertTrue(new_item.completed)  # ou False, se preferir

        # Verifica se a resposta é um redirecionamento para a página inicial
        self.assertRedirects(response, reverse('tdl:home'))

    def test_add_task_invalid_data(self):
        # Dados inválidos para o formulário (por exemplo, faltando o nome)
        form_data = {
            'name': ''  # Campo obrigatório, portanto inválido
        }

        # Envia uma requisição POST com dados inválidos
        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        # Verifica se o item não foi criado
        self.assertEqual(ItemList.objects.count(), 0)

        # Verifica se a página de formulário é renderizada novamente com erros
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add')

        # Verifica se o formulário contém o erro esperado
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['name'])

    def test_add_task_get(self):
        response = self.client.get(reverse('tdl:add_task_page'))

        # Verifica se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se o template correto está sendo usado
        self.assertTemplateUsed(response, 'tdl/partials/task_page.html')

        # Verifica se o formulário está presente no contexto
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_add_task_post_valid_data(self):
        form_data = {
            'name': 'New Task',
            'completed': True
        }

        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        # Verifica se o item foi criado
        self.assertEqual(ItemList.objects.count(), 1)
        item = ItemList.objects.first()
        self.assertEqual(item.name, 'New Task')
        self.assertTrue(item.completed)

        # Verifica o redirecionamento
        self.assertRedirects(response, reverse('tdl:home'))

    def test_add_task_post_invalid_data(self):
        form_data = {
            'name': ''  # Campo obrigatório, portanto inválido
        }

        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        # Verifica se o item não foi criado
        self.assertEqual(ItemList.objects.count(), 0)

        # Verifica se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se o template correto está sendo usado
        self.assertTemplateUsed(response, 'tdl/partials/task_page.html')

        # Verifica se o formulário contém erros
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['name'])

    def test_get_error_of_name_duplicated(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(user)

        form_data = {
            'name': 'New Task',
            'completed': True
        }

        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        self.assertRedirects(response, reverse('tdl:home'))

        response = self.client.post(reverse('tdl:add_task_page'), data=form_data)

        self.assertEqual(ItemList.objects.count(), 1)
        self.assertEqual(response.status_code, 200)


class UpdateTaskPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.item = ItemList.objects.create(name='Test Task', completed=False)

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('tdl:search')  # Gera a URL da busca sem parâmetros
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Verifica se o status é 404

    def test_search_with_empty_query(self):
        # Gere a URL com um parâmetro q vazio
        url = f'{reverse("tdl:search")}?q='
        response = self.client.get(url)

        # Verifique se a resposta está correta, por exemplo, um status 404
        self.assertEqual(response.status_code, 404)

    def test_update_task_valid_form(self):
        form_data = {
            'name': 'Updated Task'
        }
        response = self.client.post(reverse('tdl:update_task_page', args=[self.item.id]), data=form_data)

        # Verifica se o item foi atualizado
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Task')

        # Verifica se a resposta é um redirecionamento
        self.assertRedirects(response, reverse('tdl:home'))

    # def test_update_task_invalid_form(self):
    #     form_data = {
    #         'name': ''  # Campo obrigatório, portanto inválido
    #     }
    #     response = self.client.post(reverse('tdl:update_task_page', args=[self.item.id]), data=form_data)

    #     # Verifica se o item não foi atualizado
    #     self.item.refresh_from_db()
    #     self.assertEqual(self.item.name, 'Test Task')

    #     # Verifica se a página de formulário é renderizada novamente com erros
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'tdl/partials/task_page.html')

    #     # Verifica se o formulário contém erros
    #     form = response.context['form']
    #     self.assertTrue(form.errors)
    #     self.assertIn('name', form.errors)
    #     self.assertIn('Este campo é obrigatório.', form.errors['name'])
