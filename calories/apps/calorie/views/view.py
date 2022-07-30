import os

from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from calories.apps.calorie.models import NutritionalGoal
from utils.food import get_food_calories
from utils.nutritional import get_user_day_meals

fat_secret = Fatsecret(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))


@login_required
def home_view(request):
    meals = get_user_day_meals(request.user)

    total_calories = sum(filter(None, [get_food_calories(meal) for meal in meals]))
    max_calories = request.user.max_calories

    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).last()

    if goal:
        max_calories = goal.calories

    return render(request, 'calorie/home.html', context={
        'total_calories': total_calories,
        'max_calories': max_calories,
    })
