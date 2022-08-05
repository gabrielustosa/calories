from django.urls import path

from .views import (
    view,
    views_food,
    views_nutritional_goal,
    views_meal,
    views_summary,
    views_water,
    views_progress_bar,
    views_body_goal
)

app_name = 'calorie'

urlpatterns = [
    path('', view.home_view, name='home'),

    path('meal/view/', views_meal.meal_view, name='meal_view'),
    path('meal/add/', views_meal.add_meal_view, name='add_meal'),
    path('meal/manage/', views_meal.manage_meal_view, name='manage_meal'),
    path('meal/create/', views_meal.CreateMealView.as_view(), name='create_meal'),
    path('meal/delete/<int:meal_id>/', views_meal.DeleteMealView.as_view(), name='delete_meal'),
    path('meal/edit/<int:meal_id>/', views_meal.EditMealView.as_view(), name='edit_meal'),

    path('food/add/<int:meal_id>/', views_food.add_food_view, name='add_food'),
    path('food/search/<int:meal_id>/', views_food.SearchFoodView.as_view(), name='search_food'),
    path('food/render/unity/<str:food_id>/<int:meal_id>/', views_food.render_food_unity, name='render_food_unity'),
    path('food/info/<int:food_id>/', views_food.info_food_view, name='food_info'),
    path('food/create/', views_food.CreateFoodView.as_view(), name='create_food'),
    path('food/remove/<int:food_meal_id>/', views_food.remove_food_view, name='remove_food'),

    path('goal/nutritional/create/', views_nutritional_goal.CreateNutritionalGoal.as_view(), name='create_nutritional_goal'),

    path('goal/body/create/', views_body_goal.CreateBodyGoal.as_view(), name='create_body_goal'),
    path('goal/body/update/', views_body_goal.UpdateBodyGoalView.as_view(), name='update_body_goal'),
    path('goal/body/update/<int:goal_id>/', views_body_goal.UpdateBodyGoalView.as_view(), name='update_body_goal'),

    path('summary/', views_summary.food_summary_view, name='food_summary'),
    path('summary/meal_list/', views_summary.show_meal_in_range_view, name='meal_list'),
    path('summary/nutritional_info/', views_summary.render_nutritional_info_view, name='summary_nutritional_info'),
    path('summary/meal_info/<int:meal_id>/', views_summary.meal_info_view, name='summary_meal_info'),

    path('water/add/', views_water.AddWaterView.as_view(), name='add_water'),

    path('progress/render/calories/', views_progress_bar.render_progress_calories, name='render_calories_progress'),
    path('progress/render/water/', views_progress_bar.render_progress_water, name='render_water_progress'),
    path('progress/render/nutritional/', views_progress_bar.render_progress_nutritional, name='render_nutritional_progress'),
    path('progress/render/body/', views_progress_bar.render_progress_body, name='render_body_progress'),

]
