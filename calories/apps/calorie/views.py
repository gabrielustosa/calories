import os

from datetime import date

from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.forms import modelform_factory
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal, Food, FoodMeal
from utils.food import parse_food_result, get_food_calories

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

    total_calories = sum([get_food_calories(meal) for meal in meals])

    return render(request, 'calorie/home.html', context={'total_calories': total_calories})


def meal_view(request):
    today = date.today()

    meals = DayMeal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
    ).annotate(
        total_calories=Sum(
            (F('foods__serving_amount') / F('foods__food__number_of_units')) * F('foods__food__calories'))
    ).all()

    return render(request, 'calorie/includes/meal_view.html', context={'meals': meals})


def add_meal_view(request):
    meals = Meal.objects.filter(creator=request.user)
    return render(request, 'calorie/includes/add_meal.html', context={'meals': meals})


def render_create_meal_view(request):
    form = modelform_factory(Meal, fields=['name', 'time', 'icon'])
    return render(request, 'calorie/includes/create_meal.html', context={'form': form})


def create_meal_view(request):
    name = request.POST.get('name')
    time = request.POST.get('time')
    icon = request.POST.get('icon')

    Meal.objects.create(name=name, time=time, icon=icon)

    return meal_view(request)


def render_search_food_view(request, meal_id):
    today = date.today()
    meal = Meal.objects.filter(id=meal_id).first()

    day_meal = DayMeal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
        meal=meal,
    ).first()

    return render(request, 'calorie/includes/food/render_search_food.html', context={'day_meal': day_meal})


def food_search_view(request, meal_id):
    search_term = request.POST.get('search')

    foods = fat_secret.foods_search(search_term)
    return render(request, 'calorie/includes/food/search_result.html', context={'foods': foods, 'meal_id': meal_id})


def render_food_unity(request, food_id, meal_id):
    foods = []
    if not Food.objects.filter(food_id=food_id).exists():
        food_info = fat_secret.food_get_v2(food_id)

        food_result = parse_food_result(food_info)

        foods = [Food.objects.create(**food) for food in food_result]

    if not foods:
        foods = Food.objects.filter(food_id=food_id).all()

    food_info = {food.id: food.measurement_description for food in foods}

    return render(request, 'includes/modal/food_unity_body.html', context={
        'food_id': food_id,
        'meal_id': meal_id,
        'food_info': food_info,
        'first_food': list(food_info.keys())[0]
    })


def add_food_view(request, meal_id):
    day_meal = DayMeal.objects.filter(id=meal_id).first()

    serving_unity, food_id = request.POST.get('serving').split('|!')
    serving_amount = request.POST.get('serving_amount')

    food = Food.objects.filter(id=food_id).first()

    food_meal = FoodMeal.objects.create(
        serving_amount=serving_amount,
        food=food,
    )

    day_meal.foods.add(food_meal)

    return render_search_food_view(request, day_meal.meal.id)

def teste():
    pass