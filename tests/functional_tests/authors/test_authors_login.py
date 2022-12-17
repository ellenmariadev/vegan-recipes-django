import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthrosLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'Password1234'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Nome de Usuário')
        password_field = self.get_by_placeholder(form, 'Senha')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Submit form
        form.submit()

        # Success message

        self.assertIn('Login efetuado com sucesso.',
                      self.browser.find_element(By.TAG_NAME, 'body').text
                      )
        # end test
        self.sleep()

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))
        self.sleep()

        self.assertIn(
            'Not Found', self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # Open login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User see login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Try submit empty values
        username = self.get_by_placeholder(form, 'Nome de Usuário')
        password = self.get_by_placeholder(form, 'Senha')

        username.send_keys('')
        password.send_keys('')

        # Submit form
        form.submit()

        # See error message
        self.assertIn('Nome de usuário ou senha incorretos.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
