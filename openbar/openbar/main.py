from django.contrib.auth.models import User
from django.shortcuts import render
from openbar_users.forms import LoginForm
from openbar_users.models import Folder, Searcher

__author__ = 'westonnovelli'

def get_score_rank():
    scores = []
    for i in range(5):
        scores.append(booze_convert(i))
    return scores


def booze_convert(level, num_to_drink=True):
    constant = 1
    score_map = {0: 'Coke', 1: 'Light Beer', 2: 'Wine', 3: 'Tequila', 4: 'Everclear'}
    count = 0
    score = constant
    if num_to_drink:
        while score <= level:
            count += 1
            score += constant
        return score_map[count]

def index(request):
    """Render root landing page from template"""
    data = {'login_form': LoginForm(), 'ordered_score_list': get_score_rank()}
    if request.user:
        user = User.custom_objects.get_or_none(username=request.user)
        owner = Searcher.objects.get_or_none(user_profile=user)
        if owner is not None:
            data['folders'] = Folder.objects.get_or_none(owner=owner, parent=None).children.all()
    return render(request, 'index.html', data)


def animate(request):
    """Render root landing page from template"""
    data = {'login_form': LoginForm()}
    if request.user:
        user = User.custom_objects.get_or_none(username=request.user)
        owner = Searcher.objects.get_or_none(user_profile=user)
        if owner is not None:
            data['folders'] = Folder.objects.get_or_none(owner=owner, parent=None).children.all()
    return render(request, 'animate.html', data)
