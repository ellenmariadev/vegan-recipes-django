from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('Nenhuma receita publicada 😥', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        # User open the page
        self.browser.get(self.live_server_url)

        # See search field with the text 'Pesquisar...'
        search_input = self.browser.find_element(
            By.XPATH, "//input[@placeholder='Pesquisar...']")

        # Click and type search term 'Recipe title 1'
        # search_input.click()
        search_input.send_keys(recipes[1].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn('Recipe Title 1', self.browser.find_element(
            By.TAG_NAME, 'body').text)

        self.sleep()

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()
        # User open the page
        self.browser.get(self.live_server_url)

        # See pagination and go to page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Vá para a página 2"]'
        )
        page2.click()

        # See two more recipes in page 2
        self.assertEqual(len(self.browser.find_elements(
            By.CLASS_NAME, 'recipe'
        )), 2)

        self.sleep(5)
