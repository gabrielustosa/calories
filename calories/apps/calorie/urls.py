from django.urls import path

from .views import (
    view,
    views_food,
    views_goal,
    views_meal,
    views_summary,
    views_water,
    views_progress_bar,
)

app_name = 'calorie'

urlpatterns = [
    path('', view.home_view, name='home'),

    path('meal/view/', views_meal.meal_view, name='meal_view'),
    path('meal/add/', views_meal.add_meal_view, name='add_meal'),
    path('meal/render/create/', views_meal.render_create_meal_view, name='render_create_meal'),
    path('meal/create/', views_meal.create_meal_view, name='create_meal'),

    path('food/render/search/<int:meal_id>', views_food.render_search_food_view, name='render_search_food'),
    path('food/add/<int:meal_id>/', views_food.add_food_view, name='add_food'),
    path('food/search/<int:meal_id>/', views_food.food_search_view, name='food_search'),
    path('food/render/unity/<str:food_id>/<int:meal_id>/', views_food.render_food_unity, name='render_food_unity'),
    path('food/info/<int:food_id>/', views_food.info_food_view, name='food_info'),
    path('food/render/create/', views_food.render_create_food_view, name='render_create_food'),
    path('food/create/', views_food.create_food_view, name='create_food'),

    path('goal/render/create/', views_goal.render_create_goal_view, name='render_create_goal'),
    path('goal/create/', views_goal.create_goal_view, name='create_goal'),

    path('summary/', views_summary.food_summary_view, name='food_summary'),
    path('summary/meal_list/', views_summary.show_meal_in_range_view, name='meal_list'),
    path('summary/nutritional_info/', views_summary.render_nutritional_info_view, name='summary_nutritional_info'),
    path('summary/meal_info/<int:meal_id>/', views_summary.meal_info_view, name='summary_meal_info'),

    path('water/render/add/', views_water.render_add_water_view, name='render_add_water'),
    path('water/add/', views_water.add_water_view, name='add_water'),

    path('progress/render/calories/', views_progress_bar.render_progress_calories, name='render_calories_progress'),
    path('progress/render/water/', views_progress_bar.render_progress_water, name='render_water_progress'),
    path('progress/render/nutritional/', views_progress_bar.render_progress_nutritional, name='render_nutritional_progress'),
    path('progress/render/body/', views_progress_bar.render_progress_body, name='render_body_progress'),

]
