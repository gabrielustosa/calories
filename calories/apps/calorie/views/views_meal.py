from datetime import date

from django.db.models import F, Sum
from django.forms import modelform_factory
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal


def meal_view(request):
    today = date.today()

    meals = DayMeal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
    ).annotate(
        total_calories=Sum(
            (F('foods__serving_amount') / F('foods__food__number_of_units')) * F('foods__food__calories'))
    ).all()

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

    return meal_view(request)
