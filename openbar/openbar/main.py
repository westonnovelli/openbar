from django.contrib.auth.models import User
from django.shortcuts import render
from openbar_users.forms import LoginForm
from openbar_users.models import Folder, Searcher

__author__ = 'westonnovelli'

def index(request):
    """Render root landing page from template"""
    data = {'login_form': LoginForm()}
    if request.user:
        user = User.custom_objects.get_or_none(username=request.user)
        owner = Searcher.objects.get_or_none(user_profile=user)
        if owner is not None:
            data['folders'] = Folder.objects.get_or_none(owner=owner, parent=None).children.all()
    return render(request, 'index.html', data)
