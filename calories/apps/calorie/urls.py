from django.urls import path

from . import views

app_name = 'calorie'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('meal/view/', views.meal_view, name='meal_view'),
    path('meal/add/', views.add_meal_view, name='add_meal'),
    path('meal/render/create/', views.render_create_meal_view, name='render_create_meal'),
    path('meal/create/', views.create_meal_view, name='create_meal'),

    path('food/render/add/<int:meal_id>', views.render_add_food_view, name='render_add_food'),
    path('food/add/', views.add_food_view, name='add_food'),
    path('food/search/', views.food_search_view, name='food_search'),
]
