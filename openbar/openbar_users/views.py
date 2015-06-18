from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import LoginForm, SearcherForm
from django.contrib.auth.models import User
from models import Searcher

def app_login(request):
    print 'logging in'
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            name = login_form.cleaned_data['name']
            user = authenticate(username=name)
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                print "User doesn't exist"
    return render(request, 'index.html')


def login_page(request):
    login_form = LoginForm()
    return render(request, 'login/login.html', {'login_form': login_form})

def app_logout(request):
    print 'logging out'
    logout(request)
    return HttpResponseRedirect("/")

def create_account(request, success=None, error=None):
    searcher_form = SearcherForm()
    users = [user.username for user in User.objects.all()]
    return render(request, 'users/create_account.html', {'searcher_url': 'searcher/new', 'searcher_form': searcher_form,
                                                         'success': success, 'error': error, 'users': users})

def create_searcher(request):
    if request.method == 'POST':
        searcher_form = SearcherForm(request.POST or None)
        if searcher_form.is_valid():
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
