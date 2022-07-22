from django.urls import path

from . import views

app_name = 'calorie'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('meal/view/', views.meal_view, name='meal_view'),
    path('meal/add/', views.add_meal_view, name='add_meal'),
]
