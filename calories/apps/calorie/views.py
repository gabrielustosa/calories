import os

from datetime import date

from django.http import JsonResponse
from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.forms import modelform_factory
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal, Food, FoodMeal, Goal, DayGoal
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
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    Meal.objects.create(**items)

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
    today = date.today()

    day_meal = DayMeal.objects.filter(id=meal_id).first()

    serving_unity, food_id = request.POST.get('serving').split('|!')
    serving_amount = request.POST.get('serving_amount')

    food = Food.objects.filter(id=food_id).first()

    food_meal = FoodMeal.objects.create(
        serving_amount=serving_amount,
        food=food,
    )

    day_meal.foods.add(food_meal)

    day_goal = DayGoal.objects.filter(
        creator=request.user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
    ).first()

    if day_goal:
        options = ('protein', 'carbohydrate', 'fat')

        for option in options:
            food_nutrient = getattr(food, option)
            food_amount = food.number_of_units
            multiplier = int(serving_amount) / food_amount
            total = (multiplier * food_nutrient) + getattr(day_goal, option)
            setattr(day_goal, option, total)

        day_goal.save()

    return render_search_food_view(request, day_meal.meal.id)


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


def get_food_nutritional_values(request, food_id):
    food = Food.objects.filter(id=food_id).first()

    options = ('protein', 'carbohydrate', 'fat', 'calories')

    if not Goal.objects.filter(creator=request.user).exists():
        options = ('calories',)

    amount = int(request.GET.get('amount'))

    result = dict()
    for option in options:
        food_nutrient = getattr(food, option)
        food_amount = food.number_of_units
        multiplier = amount / food_amount
        total = multiplier * food_nutrient

        result[option] = total

    return JsonResponse(result)


def info_food_view(request, food_id):
    food = FoodMeal.objects.filter(id=food_id).first()

    all_nutrients = {'fat': 'Gordura', 'saturated_fat': 'Gordura Saturada',
                     'polyunsaturated_fat': 'Gordura Polisaturada', 'monounsaturated_fat': 'Gordura Monosaturada',
                     'trans_fat': 'Gordura Trans', 'cholesterol': 'Colesterol', 'sodium': 'Sódio',
                     'potassium': 'Potássio', 'fiber': 'Fibra', 'sugar': 'Açúcar',
                     'added_sugars': 'Açúcares adicionais', 'vitamin_d': 'Vítamina D', 'vitamin_a': 'Vítamina A',
                     'vitamin_c': 'Vítamina C', 'calcium': 'Cálcio', 'iron': 'Ferro'}

    return render(request, 'includes/modal/food_info_body.html',
                  context={'meal_food': food, 'all_nutrients': all_nutrients})
