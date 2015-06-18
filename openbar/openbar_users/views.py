from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import LoginForm, SearcherForm
from django.contrib.auth.models import User
from models import Searcher

def app_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['Name']
            user = authenticate(username=username)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect_to_page()
            else:
                print "User doesn't exist"
    return login(request)


def login(request):
    login_form = LoginForm()
    return render(request, 'login/login.html', {'login_form': login_form})

def app_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def redirect_to_page():
    url = "/"
    return HttpResponseRedirect(url)

def create_account(request, success=None, error=None):
    searcher_form = SearcherForm()
    return render(request, 'users/create_account.html', {'searcher_url': 'searcher/new', 'searcher_form': searcher_form,
                                                         'success': success, 'error': error})

def create_searcher(request):
    if request.method == 'POST':
        searcher_form = SearcherForm(request.POST or None)
        if searcher_form.is_valid():
            user = User(username=searcher_form.cleaned_data['name'])
            try:
                user.save()
            except IntegrityError:
                error = {"text": "User "+user.username+" already exists"}
                return create_account(request, error)
            searcher = Searcher(user_profile=user)
            searcher.save()
            success = {"text": "new account created for "+user.username}
    return render(request, 'index.html', {'success': success})
