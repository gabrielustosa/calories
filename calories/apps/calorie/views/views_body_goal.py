from django.forms import modelform_factory
from django.shortcuts import render, redirect

from calories.apps.calorie.models import BodyGoal, BodyDayGoal
from utils.nutritional import get_body_day_goal_query


def render_create_body_goal(request):
    form = modelform_factory(BodyGoal, exclude=('creator', 'active'))
    return render(request, 'calorie/includes/body_goal/render_create.html', context={'form': form})


def create_body_goal(request):
    BodyGoal.objects.filter(creator=request.user, active=True).update(active=False)

    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    goal = BodyGoal.objects.create(**items)

    day_goal = BodyDayGoal.objects.create(goal=goal)

    past_day_goal = get_body_day_goal_query(request.user).first()

    if past_day_goal:
        options = ('weight', 'fat_body', 'muscle')

        for option in options:
            setattr(day_goal, option, getattr(past_day_goal, option))

        day_goal.save()
        past_day_goal.delete()

    return redirect('/')


def render_update_body_goal(request):
    goal = get_body_day_goal_query(request.user).first()
    form = modelform_factory(BodyDayGoal, exclude=('creator', 'goal'))(instance=goal)

    return render(request, 'calorie/includes/body_goal/render_update.html', context={'form': form, 'goal_id': goal.id})


def update_body_goal(request, goal_id):
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    BodyDayGoal.objects.filter(id=goal_id).update(**items)

    return redirect('/')
