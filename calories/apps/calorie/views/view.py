import os

from datetime import date

from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal, Goal, DayGoal
from utils.food import get_food_calories

fat_secret = Fatsecret(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))


@login_required
def home_view(request):
    today = date.today()
    user_meals = Meal.objects.filter(creator=request.user)
    meals = []

    for meal in user_meals.all():
        meal_query = DayMeal.objects.filter(
            creator=request.user,
            created__year=today.year,
            created__month=today.month,
            created__day=today.day,
            meal=meal,
        )

        if meal_query.exists():
            today_meal = meal_query.annotate(
                total_calories=Sum(
                    (F('foods__serving_amount') / F('foods__food__number_of_units')) * F('foods__food__calories'))
            ).first()
        else:
            today_meal = DayMeal.objects.create(meal=meal)
        meals.append(today_meal)

    total_calories = sum(filter(None, [get_food_calories(meal) for meal in meals]))

    goal = Goal.objects.filter(creator=request.user).first()

    options = ('protein', 'carbohydrate', 'fat')

    goal_info = dict()
    if goal:
        day_goal_query = DayGoal.objects.filter(
            creator=request.user,
            created__year=today.year,
            created__month=today.month,
            created__day=today.day,
        )

        if day_goal_query.exists():
            day_goal = day_goal_query.first()
        else:
            day_goal = DayGoal.objects.create()

        for option in options:
            goal_info[f'#{option}'] = [getattr(day_goal, option), getattr(goal, option)]

    if not goal_info:
        for option in options:
            goal_info[f'#{option}'] = [0, 0]

    return render(request, 'calorie/home.html', context={
        'total_calories': total_calories,
        'goal_info': goal_info,
    })
