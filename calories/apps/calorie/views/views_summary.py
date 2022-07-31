from django.shortcuts import render

from calories.apps.calorie.models import DayMeal, NutritionalDayGoal, NutritionalGoal
from utils.food import get_nutritional_values
from utils.nutritional import get_nutrient_value, get_nutritional_day_goal_query
from utils.utils import convert_date, get_date


def food_summary_view(request):
    return render(request, 'calorie/includes/summary/view.html')


def show_meal_in_range_view(request):
    start_date = convert_date(request.GET.get('startDate'))
    end_date = convert_date(request.GET.get('endDate'))

    meals = DayMeal.objects.filter(creator=request.user, created__range=[start_date, end_date])

    return render(request, 'calorie/includes/summary/meal_list.html', context={'meals': meals})


def render_nutritional_info_view(request):
    start_date = convert_date(request.GET.get('startDate'))
    end_date = convert_date(request.GET.get('endDate'))

    nutritional_values = NutritionalDayGoal.objects.filter(creator=request.user, created__range=[start_date, end_date])

    options = ('calories', 'protein', 'carbohydrate', 'fat', 'water')

    result = {}
    for option in options:
        for nutritional_value in nutritional_values:
            result[option] = result.get(option, 0) + getattr(nutritional_value, option)

    return render(request, 'calorie/includes/summary/nutritional_info.html', context={
        'result': result,
        'start_date': get_date(start_date),
        'end_date': get_date(end_date),
    })


def meal_info_view(request, meal_id):
    day_meal = DayMeal.objects.filter(id=meal_id).first()

    main_nutrients = ('calories', 'carbohydrate', 'protein')
    other_nutrients = get_nutritional_values(exclude=main_nutrients)

    result_main_nutrients = {}
    result_other_nutrients = {}
    for food_meal in day_meal.foods.all():
        for main_nutrient in main_nutrients:
            result_main_nutrients[main_nutrient] = result_main_nutrients.get(main_nutrient, 0) + get_nutrient_value(food_meal, main_nutrient)
        for other_nutrient in other_nutrients:
            result_other_nutrients[other_nutrient] = result_other_nutrients.get(other_nutrient, 0) + get_nutrient_value(food_meal, other_nutrient)

    nutritional_goal_values = {}

    day_goal = get_nutritional_day_goal_query(request.user, datetime=day_meal.created).first()
    goal = day_goal.goal

    options = ('carbohydrate', 'calories', 'fat', 'water', 'protein')

    for option in options:
        day_goal_nutrient = getattr(day_goal, option)
        goal_nutrient = getattr(goal, option)

        if day_goal_nutrient > goal_nutrient:
            difference = day_goal_nutrient - goal_nutrient
            css_class = 'text-green-500' if option in ('water', 'protein') else 'text-red-500'
            span = f'<span class="{css_class}">{goal_nutrient}/{goal_nutrient} (+{difference})</span>'
            nutritional_goal_values[option] = span
            continue

        span = f'<span>{day_goal_nutrient}/{goal_nutrient}</span>'
        nutritional_goal_values[option] = span

    return render(request, 'includes/modal/meal_info_body.html', context={
        'day_meal': day_meal,
        'result_main_nutrients': result_main_nutrients,
        'result_other_nutrients': result_other_nutrients,
        'nutritional_goal_values': nutritional_goal_values,
    })
