from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from forms import LoginForm, SearcherForm, FolderForm
from models import Searcher, Folder
from openbar_search.forms import PreferenceForm
from openbar_search.models.results_models import Preference, Query


@login_required
def home_view(request):
    searcher = Searcher.objects.filter(user_profile=request.user)
    preferences = Preference.objects.filter() #searcher=searcher)
    folders = Folder.objects.filter(owner=searcher)
    return render(request, 'users/home.html', {'preferences': preferences,
                                               'preference_form': PreferenceForm(),
                                               'folder_form': FolderForm(),
                                               'folders': folders})


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


def create_account(request):
    searcher_form = SearcherForm()
    users = [user.username for user in User.objects.all()]
    login_form = LoginForm()
    return render(request, 'users/create_account.html', {'searcher_url': 'searcher/new', 'searcher_form': searcher_form,
                                                         'users': users, 'login_form': login_form})

def create_searcher(request):
    searcher_form = SearcherForm(request.POST or None)
    if searcher_form is not None and searcher_form.is_valid():
        name = searcher_form.cleaned_data['name']
        user = User.custom_objects.get_or_none(username=name)
        if not user:
            user = User(username=name)
            user.save()
            searcher = Searcher(user_profile=user)
            root_folder = Folder(title="root", owner=searcher)
            root_folder.save()
            searcher.save()
        else:
            return create_account(request)
    login_form = LoginForm()
    return render(request, 'index.html', {'login_form': login_form})


@login_required
def create_folder(request, internal=False):
    folder_form = FolderForm(request.POST or None)
    if folder_form is not None and folder_form.is_valid():
        title = folder_form.cleaned_data['title']
        owner = Searcher.objects.filter(user_profile=request.user)[0]
        new_folder = Folder(title=title, owner=owner)
        new_folder.save()
    else:
        print "error"
    if internal:
        return new_folder
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_subfolder(request):
    folder = create_folder(request, True)
    parent_id = request.POST['parent']
    parent = Folder.objects.get_or_none(id=parent_id)
    folder.parent = parent
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_item(request):
    query = Query.objects.get_or_none(id=request.POST['query'])
    parent = Folder.objects.get_or_none(id=request.POST['parent'])
    if query is not None and parent is not None:
        parent.items.add(query)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_item(request):
    query = Query.objects.get_or_none(id=request.POST['query'])
    parent = Folder.objects.get_or_none(id=request.POST['parent'])
    if query is not None and parent is not None:
        parent.items.remove(query)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_subfolder(request):
    folder = Folder.objects.get_or_none(id=request.POST['folder'])
    folder.parent = None
    folder.delete()
