# Generated by Django 4.0.6 on 2022-07-28 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorie', '0003_goal_daygoal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='added_sugars',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='calcium',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='carbohydrate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='cholesterol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fiber',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='iron',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='monounsaturated_fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='number_of_units',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='food',
            name='polyunsaturated_fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='potassium',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='protein',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='saturated_fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='sodium',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='sugar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='trans_fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='vitamin_a',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='vitamin_c',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='vitamin_d',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]
