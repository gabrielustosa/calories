from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from calories.apps.calorie.models import Meal
from utils.nutritional import get_user_day_meals


def meal_view(request):
    meals = get_user_day_meals(request.user)
    return render(request, 'calorie/includes/meal/view.html', context={'meals': meals})


def add_meal_view(request):
    meals = Meal.objects.filter(creator=request.user).order_by('time')
    return render(request, 'calorie/includes/meal/add.html', context={'meals': meals})


def render_create_meal_view(request):
    form = modelform_factory(Meal, exclude=('creator',))
    return render(request, 'calorie/includes/meal/create.html', context={'form': form})


def create_meal_view(request):
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    Meal.objects.create(**items)

    return redirect(reverse('calorie:home'))


def manage_meal_view(request):
    meals = Meal.objects.filter(creator=request.user).order_by('time')
    return render(request, 'calorie/includes/meal/manage.html', context={'meals': meals})


def confirm_delete_view(request, meal_id):
    confirm_text = _('Você tem certeza que deseja apagar essa refeição?')
    action_url = f'/meal/delete/{meal_id}/'
    action_target = '#content'

    return render(request, 'includes/modal/confirm_body.html', context={
        'confirm_text': confirm_text,
        'action_url': action_url,
        'action_target': action_target
    })


def remove_meal_view(request, meal_id):
    Meal.objects.filter(id=meal_id).update(creator=None)
    return manage_meal_view(request)


def render_edit_meal_view(request, meal_id):
    meal = Meal.objects.filter(id=meal_id).first()
    form = modelform_factory(Meal, exclude=('creator',))(instance=meal)
    return render(request, 'calorie/includes/meal/render_edit.html', context={'form': form, 'meal_id': meal_id})


def edit_meal_view(request, meal_id):
    items = request.POST.dict()
    del items['csrfmiddlewaretoken']

    Meal.objects.filter(id=meal_id).update(**items)

    return manage_meal_view(request)
