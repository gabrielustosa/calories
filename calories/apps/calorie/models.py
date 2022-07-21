from django.db import models
from django.utils.translation import gettext_lazy as _

from calories.apps.core.models import CreatorBase, TimeStampedBase


class Food(models.Model):
    name = models.CharField(max_length=100)
    amount_g = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    calories = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    protein = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    polyunsaturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    monounsaturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    trans_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sodium = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    potassium = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    added_sugars = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    vitamin_d = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    vitamin_a = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    vitamin_c = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    calcium = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    iron = models.DecimalField(max_digits=5, decimal_places=2, null=True)


class FoodMeal(models.Model):
    SERVING_UNITS = (
        ('G', _('Gramas')),
        ('KG', _('Kilos')),
        ('ML', _('Mililitros')),
        ('L', _('Litros')),
    )
    serving_unit = models.CharField(max_length=5, choices=SERVING_UNITS)
    serving_amount = models.DecimalField(max_digits=10, decimal_places=1)
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )


class Meal(CreatorBase):
    name = models.CharField(max_length=100)
    horario = models.TimeField()


class DayMeal(CreatorBase, TimeStampedBase):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE
    )
    foods = models.ManyToManyField(FoodMeal)
