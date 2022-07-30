from datetime import date

from django.db.models import F, Sum

from calories.apps.calorie.models import DayMeal, Meal


def get_user_day_meals(user):
    today = date.today()

    user_meals = Meal.objects.filter(creator=user)
    meals = []

    for meal in user_meals.all():
        meal_query = DayMeal.objects.filter(
            creator=user,
            created__year=today.year,
            created__month=today.month,
            created__day=today.day,
            meal=meal,
        ).prefetch_related('foods')

        if meal_query.exists():
            today_meal = meal_query.annotate(
                total_calories=Sum(
                    (F('foods__serving_amount') / F('foods__food__number_of_units')) * F('foods__food__calories'))
            ).first()
        else:
            today_meal = DayMeal.objects.create(meal=meal)
        meals.append(today_meal)

    return meals


def get_user_day_nutrients(user, nutrients):
    meals = get_user_day_meals(user)

    result = {}

    for meal in meals:
        for meal_food in meal.foods.all():
            for nutrient in nutrients:
                nutrient_value = get_nutrient_value(meal_food, nutrient)
                result[nutrient] = result.get(nutrient, 0) + nutrient_value

    return result


def get_nutrient_value(meal_food, name):
    food = meal_food.food
    food_nutrient = getattr(food, name)
    food_amount = food.number_of_units
    multiplier = meal_food.serving_amount / food_amount
    return multiplier * food_nutrient
