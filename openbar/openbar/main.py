from django.shortcuts import render
from openbar_users.forms import LoginForm

__author__ = 'westonnovelli'

def index(request):
    """Render root landing page from template"""
    login_form = LoginForm()
    return render(request, 'index.html', {'login_form': login_form})
