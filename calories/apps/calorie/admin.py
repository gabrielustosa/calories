from django.contrib import admin

from calories.apps.calorie.models import DayMeal, Food, Meal, FoodMeal, Goal, DayGoal

admin.site.register(DayMeal)
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(FoodMeal)
admin.site.register(Goal)
admin.site.register(DayGoal)