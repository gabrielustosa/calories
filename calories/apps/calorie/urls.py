from django.urls import path

from . import views

app_name = 'calorie'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('meal/view/', views.meal_view, name='meal_view'),
    path('meal/add/', views.add_meal_view, name='add_meal'),
    path('meal/render/create/', views.render_create_meal_view, name='render_create_meal'),
    path('meal/create/', views.create_meal_view, name='create_meal'),

    path('food/render/search/<int:meal_id>', views.render_search_food_view, name='render_search_food'),
    path('food/add/<int:meal_id>/', views.add_food_view, name='add_food'),
    path('food/search/<int:meal_id>/', views.food_search_view, name='food_search'),
    path('food/render/unity/<int:food_id>/<int:meal_id>/', views.render_food_unity, name='render_food_unity'),
]
