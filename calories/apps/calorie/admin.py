from django.contrib import admin

from calories.apps.calorie.models import DayMeal, Food, Meal

admin.site.register(DayMeal)
admin.site.register(Food)
admin.site.register(Meal)
