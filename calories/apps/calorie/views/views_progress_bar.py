from django.shortcuts import render

from calories.apps.calorie.models import NutritionalGoal, NutritionalDayGoal
from utils.nutritional import (
    get_current_calories,
    get_max_calories,
    get_current_water,
    get_max_water,
    get_nutritional_day_goal_query
)


def render_progress_calories(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).first()

    current_calories = get_current_calories(request.user, goal)
    max_calories = get_max_calories(goal)

    return render(request, 'includes/progressbars/calories.html', context={
        'current_calories': current_calories,
        'max_calories': max_calories,
    })


def render_progress_water(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).first()

    current_water = get_current_water(request.user)
    total_water = get_max_water(goal)

    return render(request, 'includes/progressbars/water.html', context={
        'current_water': current_water,
        'total_water': total_water,
    })


def render_progress_nutritional(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).last()

    options = ('protein', 'carbohydrate', 'fat')

    goal_info = dict()
    if goal:
        day_goal_query = get_nutritional_day_goal_query(request.user)

        if day_goal_query.exists():
            day_goal = day_goal_query.first()
        else:
            day_goal = NutritionalDayGoal.objects.create(goal=goal)

        for option in options:
            goal_info[f'#{option}'] = [round(getattr(day_goal, option)), round(getattr(goal, option))]

    if not goal_info:
        for option in options:
            goal_info[f'#{option}'] = [0, 0]

    return render(request, 'includes/progressbars/nutritional.html', context={'goal_info': goal_info})


def render_progress_body(request):
    return render(request, 'includes/progressbars/body.html')
