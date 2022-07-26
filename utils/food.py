from typing import Dict

nutritional_info = (
    'calories', 'carbohydrate', 'protein', 'fat',
    'saturated_fat', 'polyunsaturated_fat', 'monounsaturated_fat',
    'trans_fat', 'cholesterol', 'sodium', 'potassium', 'fiber',
    'sugar', 'added_sugars', 'vitamin_d', 'vitamin_a',
    'vitamin_c', 'calcium', 'iron'
)


def parse_food_result(food_dict: Dict, serving_unity: str):
    result = dict()

    if serving_unity == 'kg':
        serving_unity = 'g'
    if serving_unity == 'l':
        serving_unity = 'ml'

    for serving in food_dict['servings']['serving']:
        if serving['measurement_description'] == serving_unity:
            for nutricional, nutricional_value in serving.items():
                if nutricional in nutritional_info:
                    result[nutricional] = nutricional_value

    result['name'] = food_dict['food_name']

    return result
