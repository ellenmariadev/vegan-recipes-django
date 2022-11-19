from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'title': 'Receitas',
        'cssfile': 'home.css'
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-detail.html', context={
        'title': 'Receitas'
    })
