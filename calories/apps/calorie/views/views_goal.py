from datetime import date

from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse

from calories.apps.calorie.models import Goal, DayGoal


def render_create_goal_view(request):
    form = modelform_factory(Goal, exclude=('goal',))
    return render(request, 'calorie/includes/goal/create_goal.html', context={'form': form})


def create_goal_view(request):
    today = date.today()

    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    goal = Goal.objects.create(**items)

    day_goal_query = DayGoal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
    )

    if not day_goal_query.exists():
        DayGoal.objects.create(goal=goal)

    return redirect(reverse('calorie:home'))
