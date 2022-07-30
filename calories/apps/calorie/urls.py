from django.urls import path

from .views import view, views_food, views_goal, views_meal, views_summary

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
    path('food/nutritional_value/<int:food_id>/', views_food.get_food_nutritional_values, name='get_nutritional_value'),
    path('food/info/<int:food_id>/', views_food.info_food_view, name='food_info'),
    path('food/render/create/', views_food.render_create_food_view, name='render_create_food'),
    path('food/create/', views_food.create_food_view, name='create_food'),

    path('goal/render/create/', views_goal.render_create_goal_view, name='render_create_goal'),
    path('goal/create/', views_goal.create_goal_view, name='create_goal'),
    path('goal/render/bar/nutritional/', views_goal.render_goal_nutritional_bar, name='render_goal_bar_nutritional'),
    path('goal/render/bar/body/', views_goal.render_goal_body_bar, name='render_goal_bar_body'),

    path('summary/', views_summary.food_summary_view, name='food_summary'),
    path('summary/meal_list/', views_summary.show_meal_in_range_view, name='meal_list'),

]
