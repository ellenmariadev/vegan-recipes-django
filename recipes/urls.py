from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('recipes/category/<int:id>/', views.recipe_category, name='categories'),
    path('recipe/<int:id>/', views.recipe, name='recipe')
]
