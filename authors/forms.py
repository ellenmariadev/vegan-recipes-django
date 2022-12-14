import re

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Senha deve conter 8 dígitos, pelo menos uma letra maiúscula e minúscula e um número.' # noqa E501
        ), code='invalid')


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de Usuário')
        add_placeholder(self.fields['email'], 'E-mail')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha'
        }),
        error_messages={
            'required': 'Senha não pode ficar vazia.'
        },
        validators=[strong_password]
    )
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Senha'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            password_confirmation_error = ValidationError(
                'As senhas precisam estar iguais.',
                code='invalid'
            )
            raise ValidationError({
                'password_confirm': [
                    password_confirmation_error,
                ],
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Esse e-mail já está registrado.', code='invalid',
            )

        return email
