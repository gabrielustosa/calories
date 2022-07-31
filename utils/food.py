from typing import Dict

from django.utils.translation import gettext_lazy as _


def parse_food_result(food_dict: Dict):
    nutritional_info = (
        'calories', 'carbohydrate', 'protein', 'fat', 'food_name',
        'saturated_fat', 'polyunsaturated_fat', 'monounsaturated_fat',
        'trans_fat', 'cholesterol', 'sodium', 'potassium', 'fiber',
        'sugar', 'added_sugars', 'vitamin_d', 'vitamin_a', 'food_id',
        'vitamin_c', 'calcium', 'iron', 'number_of_units', 'measurement_description',
    )
    result = list()

    food_serving = food_dict['servings']['serving']

    if isinstance(food_serving, dict):
        food_serving = [food_serving]

    for serving in food_serving:
        food_info = dict()
        for nutritional, nutritional_value in serving.items():
            if nutritional in nutritional_info:
                food_info[nutritional] = nutritional_value
        result.append(food_info)

    for food in result:
        food['food_name'] = food_dict['food_name']
        food['food_id'] = food_dict['food_id']

    return result


def get_food_calories(food):
    try:
        total = food.total_calories

        return total
    except AttributeError:
        return 0


nutritional_values_translated = {
    'fat': _('Gordura'),
    'saturated_fat': _('Gordura Saturada'),
    'polyunsaturated_fat': _('Gordura Polisaturada'),
    'monounsaturated_fat': _('Gordura Monosaturada'),
    'trans_fat': _('Gordura Trans'),
    'cholesterol': _('Colesterol'),
    'sodium': _('Sódio'),
    'potassium': _('Potássio'),
    'fiber': _('Fibra'),
    'sugar': _('Açúcar'),
    'added_sugars': _('Açúcares adicionais'),
    'vitamin_d': _('Vítamina D'),
    'vitamin_a': _('Vítamina A'),
    'vitamin_c': _('Vítamina C'),
    'calcium': _('Cálcio'),
    'iron': _('Ferro'),
    'water': _('Água'),
    'protein': _('Proteína'),
    'carbohydrate': _('Carboidrato'),
    'calories': _('Calorias'),
}


def get_nutritional_translated(value):
    return nutritional_values_translated[value]


def get_nutritional_values(exclude=None):
    if not exclude:
        exclude = []
    result = []
    nutritional_info = (
        'calories', 'carbohydrate', 'protein', 'fat',
        'saturated_fat', 'polyunsaturated_fat', 'monounsaturated_fat',
        'trans_fat', 'cholesterol', 'sodium', 'potassium', 'fiber',
        'sugar', 'added_sugars', 'vitamin_d', 'vitamin_a',
        'vitamin_c', 'calcium', 'iron',
    )
    for value in nutritional_info:
        if value not in exclude:
            result.append(value)

    return result
