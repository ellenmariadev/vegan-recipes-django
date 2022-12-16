from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([('username', 'Nome de Usuário'),
                           ('email', 'E-mail'),
                           ('password', 'Senha'),
                           ('password_confirm', 'Confirmar Senha')])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([('username', 'Nome de Usuário'),
                           ('email', 'E-mail'),
                           ('password', 'Senha'),
                           ('password_confirm', 'Confirmar Senha')])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirm': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('email', 'Este campo é obrigatório.'),
        ('password', 'Este campo é obrigatório.'),
        ('password_confirm', 'Este campo é obrigatório.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'eli'
        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O nome de usuário deve ter pelo menos 4 caracteres.'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_20(self):
        self.form_data['username'] = 'E' * 21
        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O nome de usuário deve ter menos de 20 caracteres.'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_uppercase_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Sua senha deve conter no mínimo 8 caracteres com pelo menos um número, uma letra maiúscula e uma letra minúscula.'  # noqa E501

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password_confirm'] = '@A123abc1235'

        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas precisam estar iguais.'

        self.assertIn(
            msg, response.context['form'].errors.get('password_confirm'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password_confirm'] = '@A123abc123'

        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_return_404(self):
        url = reverse('create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Esse e-mail já está registrado.'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'password12345',
            'password_confirm': 'password12345',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='password12345',
        )

        self.assertTrue(is_authenticated)
