from collections import defaultdict

from django import forms
from django.forms import ValidationError

from recipes.models import Recipe
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuthorRecipeForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Título da Receita"
        self.fields['description'].label = "Descrição"
        self.fields['preparation_time'].label = "Tempo de Preparo"
        self.fields['preparation_time_unit'].label = "Unidade"
        self.fields['servings'].label = "Serve"
        self.fields['servings_unit'].label = "Unidade"
        self.fields['preparation_steps'].label = "Modo de Preparo"
        self.fields['cover'].label = "Adicionar Imagem"

        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover']

        widgets = {
            'cover': forms.FileInput(),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 4:
            self._my_errors['title'].append(
                'Deve conter pelo menos 4 caracteres.')
        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'Informe um tempo de preparo válido.')
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'Informe uma quantidade válida.')
        return field_value
