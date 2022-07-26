from django.contrib import admin

from calories.apps.calorie.models import DayMeal, Food, Meal, FoodMeal, NutritionalGoal, NutritionalDayGoal, \
    BodyDayGoal, BodyGoal

admin.site.register(DayMeal)
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(FoodMeal)
admin.site.register(NutritionalGoal)
admin.site.register(NutritionalDayGoal)
admin.site.register(BodyDayGoal)
admin.site.register(BodyGoal)