# Generated by Django 4.0.6 on 2022-07-31 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_id', models.CharField(max_length=250)),
                ('food_name', models.CharField(max_length=100)),
                ('calories', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('carbohydrate', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('protein', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('fat', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('saturated_fat', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('polyunsaturated_fat', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('monounsaturated_fat', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('trans_fat', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('cholesterol', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('sodium', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('potassium', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('fiber', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('sugar', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('added_sugars', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('vitamin_d', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('vitamin_a', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('vitamin_c', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('calcium', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('iron', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('measurement_description', models.CharField(max_length=100)),
                ('number_of_units', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionalGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein', models.PositiveIntegerField(default=0)),
                ('carbohydrate', models.PositiveIntegerField(default=0)),
                ('fat', models.PositiveIntegerField(default=0)),
                ('calories', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NutritionalDayGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateField(auto_now=True, verbose_name='Modification Date and Time')),
                ('protein', models.PositiveIntegerField(default=0)),
                ('carbohydrate', models.PositiveIntegerField(default=0)),
                ('fat', models.PositiveIntegerField(default=0)),
                ('calories', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.nutritionalgoal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time', models.TimeField()),
                ('icon', models.CharField(choices=[('Apple', 'Apple'), ('Carrot', 'Carrot'), ('Egg', 'Egg'), ('Lemon', 'Lemon'), ('Bacon', 'Bacon'), ('Chicken', 'Chicken'), ('Cheese', 'Cheese'), ('Cookie', 'Cookie'), ('Fish', 'Fish'), ('Burger', 'Burger')], max_length=100)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serving_amount', models.DecimalField(decimal_places=1, max_digits=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='calorie.food')),
            ],
        ),
        migrations.CreateModel(
            name='DayMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateField(auto_now=True, verbose_name='Modification Date and Time')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('foods', models.ManyToManyField(to='calorie.foodmeal')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.meal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
