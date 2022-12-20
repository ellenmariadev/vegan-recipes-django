from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),  # noqa E501
    path('recipes/category/<int:id>/', views.RecipeListViewCategory.as_view(), name='categories'),  # noqa E501
    path('recipe/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
]
