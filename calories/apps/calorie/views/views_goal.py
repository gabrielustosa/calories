from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse

from calories.apps.calorie.models import NutritionalGoal, NutritionalDayGoal
from utils.nutritional import get_user_day_nutrients, get_nutritional_day_goal_query


def render_create_goal_view(request):
    form = modelform_factory(NutritionalGoal, exclude=('goal', 'active'))
    return render(request, 'calorie/includes/goal/create.html', context={'form': form})


def create_goal_view(request):
    NutritionalGoal.objects.filter(creator=request.user).update(active=False)

    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    goal = NutritionalGoal.objects.create(**items)
    day_goal_query = get_nutritional_day_goal_query(request.user, goal)

    if not day_goal_query.exists():
        day_goal = NutritionalDayGoal.objects.create(goal=goal)

        nutrients = get_user_day_nutrients(request.user, ('protein', 'carbohydrate', 'fat', 'calories'))

        for nutrient, nutrient_value in nutrients.items():
            setattr(day_goal, nutrient, nutrient_value)

        day_goal.save()

    return redirect(reverse('calorie:home'))


def render_goal_nutritional_bar(request):
    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).last()

    options = ('protein', 'carbohydrate', 'fat')

    goal_info = dict()
    if goal:
        day_goal_query = get_nutritional_day_goal_query(request.user, goal)

        if day_goal_query.exists():
            day_goal = day_goal_query.first()
        else:
            day_goal = NutritionalDayGoal.objects.create(goal=goal)

        for option in options:
            goal_info[f'#{option}'] = [getattr(day_goal, option), getattr(goal, option)]

    if not goal_info:
        for option in options:
            goal_info[f'#{option}'] = [0, 0]

    return render(request, 'calorie/includes/goal/progressbars/nutritional.html', context={'goal_info': goal_info})


def render_goal_body_bar(request):
    return render(request, 'calorie/includes/goal/progressbars/body.html')
