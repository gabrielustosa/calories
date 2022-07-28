# Generated by Django 4.0.6 on 2022-07-28 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calorie', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein', models.PositiveIntegerField(default=0)),
                ('carbohydrate', models.PositiveIntegerField(default=0)),
                ('fat', models.PositiveIntegerField(default=0)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DayGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('protein', models.PositiveIntegerField(default=0)),
                ('carbohydrate', models.PositiveIntegerField(default=0)),
                ('fat', models.PositiveIntegerField(default=0)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
