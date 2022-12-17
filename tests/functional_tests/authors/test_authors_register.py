import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_data_base(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 15)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/register')
        form = self.get_form()

        self.fill_form_data_base(form)
        form.find_element(By.NAME, 'email').send_keys('email@anyemail.com')

        callback(form)

        return form

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Nome de Usuário')
            username_field.send_keys('')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.sleep()

            self.assertIn('Este campo é obrigatório.', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'E-mail')
            email_field.send_keys('')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.sleep()

            self.assertIn('Este campo é obrigatório.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Senha')
            password_field.send_keys('')
            password_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.sleep()

            self.assertIn('Este campo é obrigatório.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_confirm_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Confirmar Senha')
            password_field.send_keys('')
            password_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.sleep()

            self.assertIn('Este campo é obrigatório.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Senha')
            password2 = self.get_by_placeholder(form, 'Confirmar Senha')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('As senhas precisam estar iguais.', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/register/')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Nome de Usuário').send_keys('my_username')
        self.get_by_placeholder(
            form, 'E-mail').send_keys('email@valid.com')
        self.get_by_placeholder(
            form, 'Senha').send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form, 'Confirmar Senha').send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Conta criada com sucesso.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
