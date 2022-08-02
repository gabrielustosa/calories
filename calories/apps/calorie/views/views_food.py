from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, Meal, Food, FoodMeal, NutritionalGoal
from calories.apps.calorie.views.view import fat_secret
from calories.apps.calorie.views.views_meal import meal_view
from utils.food import parse_food_result, get_nutritional_values
from utils.nutritional import get_nutritional_day_goal_query, get_meal_day_goal_query, get_nutrient_value
from utils.utils import get_random_id


def add_food_view(request, meal_id):
    day_meal = DayMeal.objects.filter(id=meal_id).first()

    food_id = request.POST.get('serving')
    serving_amount = request.POST.get('serving_amount')

    food = Food.objects.filter(id=food_id).first()

    food_meal = FoodMeal.objects.create(
        serving_amount=serving_amount,
        food=food,
    )

    day_meal.foods.add(food_meal)

    day_goal = get_nutritional_day_goal_query(request.user).first()

    if day_goal:
        options = ('protein', 'carbohydrate', 'fat', 'calories')

        for option in options:
            total = get_nutrient_value(food_meal, option) + getattr(day_goal, option)
            setattr(day_goal, option, total)

        day_goal.save()

    return render_search_food_view(request, day_meal.meal.id)


def render_search_food_view(request, meal_id):
    meal = Meal.objects.filter(id=meal_id).first()

    day_meal = get_meal_day_goal_query(request.user, meal).first()

    return render(request, 'calorie/includes/food/search.html', context={'day_meal': day_meal})


def food_search_view(request, meal_id):
    search_term = request.POST.get('search')

    try:
        foods = fat_secret.foods_search(search_term)
    except KeyError:
        foods = []

    custom_foods = Food.objects.filter(food_id__regex=r'[a-zA-Z]', food_name__icontains=search_term)

    for custom_food in custom_foods.all():
        food_description = f'Per {custom_food.measurement_description} {custom_food.number_of_units} - Calories: {custom_food.calories:.0f}kcal | Fat: {custom_food.fat}g | Carbs: {custom_food.carbohydrate}g | Protein: {custom_food.protein}g'
        foods.append(
            {
                'food_id': custom_food.food_id,
                'food_name': custom_food.food_name,
                'food_description': food_description,
            }
        )

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
    })


def get_food_nutritional_values(request, food_id):
    food = Food.objects.filter(id=food_id).first()

    goal = NutritionalGoal.objects.filter(creator=request.user, active=True).first()
    day_goal = get_nutritional_day_goal_query(request.user).first()

    options = ('protein', 'carbohydrate', 'fat', 'calories')

    amount = int(request.GET.get('amount'))

    result = dict()
    if goal:
        for option in options:
            food_nutrient = getattr(food, option)
            food_amount = food.number_of_units
            multiplier = amount / food_amount
            total = multiplier * food_nutrient

            result[option] = total

            if day_goal:
                result[f'current-{option}'] = getattr(day_goal, option)
                result[f'total-{option}'] = getattr(goal, option)

    if not result:
        result.update({'empty': True})

    return JsonResponse(result)


def info_food_view(request, food_id):
    food = FoodMeal.objects.filter(id=food_id).first()

    main_nutrients = ('calories', 'carbohydrate', 'protein')
    other_nutrients = get_nutritional_values(exclude=main_nutrients)

    return render(request, 'includes/modal/food_info_body.html', context={
        'meal_food': food,
        'main_nutrients': main_nutrients,
        'other_nutrients': other_nutrients,
    })


def render_create_food_view(request):
    form = modelform_factory(Food, exclude=('food_id',))
    return render(request, 'calorie/includes/food/create.html', context={'form': form})


def create_food_view(request):
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    items['food_id'] = get_random_id()

    Food.objects.create(**items)

    return meal_view(request)
