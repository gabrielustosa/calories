from datetime import date

from django.forms import modelform_factory
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Goal, DayGoal
from calories.apps.calorie.views.views_meal import meal_view


def render_create_goal_view(request):
    form = modelform_factory(Goal, fields=('protein', 'carbohydrate', 'fat'))
    return render(request, 'calorie/includes/goal/create_goal.html', context={'form': form})


def create_goal_view(request):
    today = date.today()

    goal_query = Goal.objects.filter(creator=request.user)
    if goal_query.exists():
        goal_query.delete()

    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    Goal.objects.create(**items)

    day_goal_query = DayGoal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
    )

    if day_goal_query.exists():
        day_meal_query = DayMeal.objects.filter(
            creator=request.user,
            created__year=today.year,
            created__month=today.month,
            created__day=today.day,
        )
        options = ('protein', 'carbohydrate', 'fat')

        if day_meal_query.exists():
            day_goal = day_goal_query.first()
            for day_meal in day_meal_query.all():
                for food_meal in day_meal.foods.all():
                    food = food_meal.food
                    for option in options:
                        food_nutrient = getattr(food, option)
                        food_amount = food.number_of_units
                        multiplier = food_meal.serving_amount / food_amount
                        total = (multiplier * food_nutrient) + getattr(day_goal, option)
                        setattr(day_goal, option, total)
            day_goal.save()
    else:
        DayGoal.objects.create()

    return meal_view(request)
