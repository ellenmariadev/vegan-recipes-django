from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_category_string_representation(self):
        string_name = 'Testing Representation'
        self.category.name = string_name
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category), string_name,
            msg=f'Recipe string representation must be '
            f'"{string_name}" but "{str(self.category)}" was received.'
        )

    def test_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
