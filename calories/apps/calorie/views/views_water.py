from django.shortcuts import render, redirect

from utils.nutritional import get_nutritional_day_goal_query


def render_add_water_view(request):
    return render(request, 'calorie/includes/water/add.html')


def add_water_view(request):
    goal = get_nutritional_day_goal_query(request.user).first()
    goal.water = int(request.POST.get('water')) + goal.water
    goal.save()
    return redirect('/')
