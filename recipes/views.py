from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe

# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'title': 'Receitas',
        'recipes': recipes
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe.objects.filter(
        pk=id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/recipe-detail.html', context={
        'title': '',
        'recipe': recipe
    })


def recipe_category(request, id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
    })
