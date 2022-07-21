from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal


@login_required
def home_view(request):
    return render(request, 'calorie/home.html')


def meal_view(request):
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
            today_meal = meal_query.annotate(total_calories=Count('foods__calories')).first()
        else:
            today_meal = DayMeal.objects.create(meal=meal)
        meals.append(today_meal)

    return render(request, 'calorie/includes/meal_view.html', context={'meals': meals})
