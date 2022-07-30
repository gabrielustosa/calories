from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse

from calories.apps.calorie.models import Meal
from utils.nutritional import get_user_day_meals


def meal_view(request):
    meals = get_user_day_meals(request.user)

    return render(request, 'calorie/includes/meal/meal_view.html', context={'meals': meals})


def add_meal_view(request):
    meals = Meal.objects.filter(creator=request.user)
    return render(request, 'calorie/includes/meal/add_meal.html', context={'meals': meals})


def render_create_meal_view(request):
    form = modelform_factory(Meal, fields=['name', 'time', 'icon'])
    return render(request, 'calorie/includes/meal/create_meal.html', context={'form': form})


def create_meal_view(request):
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    Meal.objects.create(**items)

    return redirect(reverse('calorie:home'))
