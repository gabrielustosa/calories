from django.http import JsonResponse
from django.shortcuts import render

from calories.apps.calorie.models import NutritionalGoal
from utils.nutritional import get_nutritional_day_goal_query


def render_add_water_view(request):
    return render(request, 'calorie/includes/water/add.html')


def add_water_view(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).first()
    day_goal = get_nutritional_day_goal_query(request.user).first()
    result = dict()
    if day_goal:
        day_goal.water = int(request.GET.get('water')) + day_goal.water
        day_goal.save()
        result['current-water'] = day_goal.water
        result['total-water'] = goal.water

    if not result:
        result.update({'empty': True})

    return JsonResponse(result)
