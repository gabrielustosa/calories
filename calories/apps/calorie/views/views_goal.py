from django.forms import modelform_factory
from django.shortcuts import render, redirect

from calories.apps.calorie.models import NutritionalGoal, NutritionalDayGoal
from utils.nutritional import get_user_day_nutrients, get_nutritional_day_goal_query


def render_create_goal_view(request):
    form = modelform_factory(NutritionalGoal, exclude=('goal', 'active'))
    return render(request, 'calorie/includes/goal/create.html', context={'form': form})


def create_goal_view(request):
    NutritionalGoal.objects.filter(creator=request.user, active=True).update(active=False)

    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    goal = NutritionalGoal.objects.create(**items)

    day_goal_query = get_nutritional_day_goal_query(request.user)
    day_goal_query.delete()

    day_goal = NutritionalDayGoal.objects.create(goal=goal)

    nutrients = get_user_day_nutrients(request.user, ('protein', 'carbohydrate', 'fat', 'calories'))

    for nutrient, nutrient_value in nutrients.items():
        setattr(day_goal, nutrient, nutrient_value)

    day_goal.save()

    return redirect('/')
