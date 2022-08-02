import os

from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from calories.apps.calorie.models import NutritionalGoal
from utils.nutritional import get_current_calories, get_max_calories, get_current_water, get_max_water

fat_secret = Fatsecret(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))


@login_required
def home_view(request):
    return render(request, 'calorie/home.html')


def render_progress_circle(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).first()

    current_calories = get_current_calories(request.user, goal)
    max_calories = get_max_calories(goal)

    current_water = get_current_water(request.user)
    total_water = get_max_water(goal)

    return render(request, 'calorie/includes/goal/progressbars/circle.html', context={
        'current_calories': current_calories,
        'max_calories': max_calories,
        'current_water': current_water,
        'total_water': total_water,
    })
