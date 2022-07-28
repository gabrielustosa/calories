from typing import Dict

nutritional_info = (
    'calories', 'carbohydrate', 'protein', 'fat', 'food_name',
    'saturated_fat', 'polyunsaturated_fat', 'monounsaturated_fat',
    'trans_fat', 'cholesterol', 'sodium', 'potassium', 'fiber',
    'sugar', 'added_sugars', 'vitamin_d', 'vitamin_a', 'food_id',
    'vitamin_c', 'calcium', 'iron', 'number_of_units', 'measurement_description',
)


def parse_food_result(food_dict: Dict):
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
