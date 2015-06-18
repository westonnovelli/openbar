from django.contrib.auth import login, logout, authenticate
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

def create_account(request):
    searcher_form = SearcherForm()
    return render(request, 'users/create_account.html', {'searcher_url': 'searcher/new', 'searcher_form': searcher_form})

def create_searcher(request):
    if request.method == 'POST':
        searcher_form = SearcherForm(request.POST or None)
        if searcher_form.is_valid():
            user = User(username=searcher_form.cleaned_data['name'])
            user.save()
            searcher = Searcher(user_profile=user)
            searcher.save()
    return render(request, 'index.html')
