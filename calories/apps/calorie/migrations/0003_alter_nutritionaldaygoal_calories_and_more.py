# Generated by Django 4.0.6 on 2022-08-03 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorie', '0002_alter_food_food_id_alter_foodmeal_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionaldaygoal',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionaldaygoal',
            name='carbohydrate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionaldaygoal',
            name='fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionaldaygoal',
            name='protein',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalgoal',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalgoal',
            name='carbohydrate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalgoal',
            name='fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalgoal',
            name='protein',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]