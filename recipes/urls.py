from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/category/<int:id>/', views.recipe_category, name='categories'),  # noqa E501
    path('recipe/<int:id>/', views.recipe, name='recipe'),
]
