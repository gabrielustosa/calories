from django import template

register = template.Library()


@register.filter()
def get_nutrient_value(meal_food, name):
    food = meal_food.food
    food_nutrient = getattr(food, name)
    food_amount = food.number_of_units
    multiplier = meal_food.serving_amount / food_amount
    return multiplier * food_nutrient
