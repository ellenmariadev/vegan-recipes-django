from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de Usuário')
        add_placeholder(self.fields['email'], 'E-mail')

    username = forms.CharField(
        label='Nome de Usuário',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'O nome de usuário deve ter pelo menos 4 caracteres.',  # noqa E501
            'max_length': 'O nome de usuário deve ter menos de 20 caracteres.',
            'unique': 'Este nome de usuário já existe.'
        },
        min_length=4, max_length=20,
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={'required': 'Este campo é obrigatório.',
                        'invalid': 'Informe um e-mail válido.'}
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha'
        }),
        error_messages={
            'required': 'Este campo é obrigatório.',
        },
        validators=[strong_password]
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Senha',
        }),
        error_messages={
            'required': 'Este campo é obrigatório.'
        },
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
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
