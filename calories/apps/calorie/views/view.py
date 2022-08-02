import os

from fatsecret import Fatsecret

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

fat_secret = Fatsecret(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))


@login_required
def home_view(request):
    return render(request, 'calorie/home.html')
