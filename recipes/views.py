import os

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Recipe

# Create your views here.

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


@login_required(login_url='authors:login', redirect_field_name='next')
def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'title': 'Receitas',
        'recipes': page_obj,
        'pagination_range': pagination_range,
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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def search(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', context={
        'search_term': search_term,
        'title': f'Pesquisar por "{search_term}"',
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
