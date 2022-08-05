from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from calories.apps.calorie.models import BodyGoal, BodyDayGoal
from utils.nutritional import get_body_day_goal_query


class CreateBodyGoal(TemplateView):
    def get(self, request, *args, **kwargs):
        form = modelform_factory(BodyGoal, exclude=('creator', 'active'))
        return render(request, 'calorie/includes/body_goal/render_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        BodyGoal.objects.filter(creator=request.user, active=True).update(active=False)

        items = request.POST.dict()
        del items['csrfmiddlewaretoken']

        goal = BodyGoal.objects.create(**items)

        day_goal = BodyDayGoal.objects.create(goal=goal)

        past_day_goal = get_body_day_goal_query(request.user).first()

        if past_day_goal:
            options = ('weight', 'fat_body', 'muscle')

            for option in options:
                setattr(day_goal, option, getattr(past_day_goal, option))

            day_goal.save()

        return redirect('/')


class UpdateBodyGoalView(TemplateView):
    def get(self, request, *args, **kwargs):
        goal = get_body_day_goal_query(request.user).first()
        form = modelform_factory(BodyDayGoal, exclude=('creator', 'goal'))(instance=goal)

        return render(request, 'calorie/includes/body_goal/render_update.html',
                      context={'form': form, 'goal_id': goal.id})

    def post(self, request, *args, **kwargs):
        items = request.POST.dict()
        del items['csrfmiddlewaretoken']

        BodyDayGoal.objects.filter(id=self.kwargs.get('goal_id')).update(**items)

        return redirect('/')
