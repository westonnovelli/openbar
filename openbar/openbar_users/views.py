from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from forms import LoginForm, SearcherForm
from models import Searcher
from openbar_search.forms import PreferenceForm
from openbar_search.models import Preference


@login_required
def home_view(request):
    searcher = Searcher.objects.filter(user_profile=request.user)
    preferences = Preference.objects.filter(searcher=searcher)
    return render(request, 'users/home.html', {'preferences': preferences,
                                               'preference_form': PreferenceForm()})

def app_login(request):
    login_form = LoginForm(request.POST or None)
    if login_form is not None and login_form.is_valid():
        name = login_form.cleaned_data['name']
        user = authenticate(username=name)
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            print "User doesn't exist"
    return redirect(home_view)

def login_page(request):
    login_form = LoginForm()
    return render(request, 'login/login.html', {'login_form': login_form})

@login_required
def app_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def create_account(request, success=None, error=None):
    searcher_form = SearcherForm()
    users = [user.username for user in User.objects.all()]
    login_form = LoginForm()
    return render(request, 'users/create_account.html', {'searcher_url': 'searcher/new', 'searcher_form': searcher_form,
                                                         'success': success, 'error': error, 'users': users,
                                                         'login_form': login_form})

def create_searcher(request):
    searcher_form = SearcherForm(request.POST or None)
    if searcher_form is not None and searcher_form.is_valid():
        name = searcher_form.cleaned_data['name']
        user = User.custom_objects.get_or_none(username=name)
        if not user:
            user = User(username=name)
            user.save()
            searcher = Searcher(user_profile=user)
            searcher.save()
            success = {"text": "new account created for "+user.username}
        else:
            error = {"text": "User "+user.username+" already exists"}
            return create_account(request, error)
    return render(request, 'index.html', {'success': success})

