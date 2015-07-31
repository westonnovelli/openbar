import random

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from forms import LoginForm, SearcherForm, FolderForm
from models import Searcher, Folder, FollowedLink
from openbar.global_follow import get_followed_links
from openbar.main import index
from openbar_search.forms import PreferenceForm
from openbar_search.models import Preference, Query, BoozeComplexityScore


@login_required
def home_view(request):
    searcher = Searcher.objects.filter(user_profile=request.user)
    preferences = Preference.objects.filter()  #searcher=searcher)
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
    return redirect(index)


def login_page(request):
    return redirect(index)


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
            root_folder = Folder(title="Bookmarks", owner=searcher)
            root_folder.save()
            complexity_score = BoozeComplexityScore.objects.create(level=random.randint(0, 4))
            searcher.complexity_score = complexity_score
            print searcher
            searcher.save()
        else:
            return create_account(request)
    return redirect(index)

@login_required
def update_score(request):
    searcher = get_searcher(request)
    complexity_score = BoozeComplexityScore.objects.create(level=random.randint(0, 4))
    searcher.complexity_score = complexity_score
    searcher.save()
    return redirect(index)


@login_required
@csrf_exempt
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


@login_required
@csrf_exempt
def add_subfolder(request):
    folder = create_folder(request, True)
    parent_id = request.GET['parent']
    parent = Folder.objects.get_or_none(id=parent_id)
    folder.parent = parent
    folder.save()


@login_required
@csrf_exempt
def add_item(request):
    query = Query.objects.get_or_none(id=request.GET['query'])
    parent = Folder.objects.get_or_none(id=request.GET['parent'])
    if query is not None and parent is not None:
        parent.items.add(query)
        parent.save()
    if request.GET['ajax_source']:

        return render(request, "users/folders.html", {'folders': [get_folders_data(request)], 'dropdown': True})


@login_required
@csrf_exempt
def remove_item(request):
    query = Query.objects.get_or_none(id=request.GET['query'])
    parent = Folder.objects.get_or_none(id=request.GET['parent'])
    if query is not None and parent is not None:
        parent.items.remove(query)
        parent.save()
    if request.GET['ajax_source']:
        return render(request, "users/folders.html", {'folders': [get_folders_data(request)], 'dropdown': True})


@login_required
@csrf_exempt
def remove_subfolder(request):
    folder = Folder.objects.get_or_none(id=request.GET['folder'])
    folder.parent = None
    folder.delete()


def get_folders_data(request):
    try:
        username = request.GET['user']
    except:
        username = request.user
    user_profile = User.custom_objects.get_or_none(username=username)
    if user_profile is not None:
        searcher = Searcher.objects.get_or_none(user_profile=user_profile)
        if searcher is not None:
            root = Folder.objects.get_or_none(owner=searcher, parent=None)
            if root is not None:
                return root


@csrf_exempt
def get_folders(request):
    root = get_folders_data(request)
    if root is not None:
        return render(request, 'users/folders.html', {'folders': [root]})
    print "fail"
    return redirect(index)

@csrf_exempt
def get_user_complexity_score(request):
    user_profile = User.custom_objects.get_or_none(username=request.user)
    if user_profile is not None:
        searcher = Searcher.objects.get_or_none(user_profile=user_profile)
        if searcher is not None:
            return render(request, 'cs.html', {'cs': searcher.complexity_score.show()})
    return render(request, 'cs.html', {'cs': ""})

def get_searcher(request):
    return Searcher.objects.get_or_none(user_profile=request.user.id)

@login_required
@csrf_exempt
def follow_link(request):
    searcher = get_searcher(request)
    if searcher is not None:
        query = Query.objects.get(id=request.GET['query'])
        followed_link = FollowedLink(link=query, owner=searcher)
        followed_link.save()
    return render(request, 'users/links_followed.html', {'followed_links': get_followed_links(searcher)})


@login_required
@csrf_exempt
def reviewed_link(request):
    followed_link = FollowedLink.objects.get(id=request.GET['id'])
    followed_link.reviewed = True
    followed_link.save()
    owner = get_searcher(request)
    return render(request, 'users/links_followed.html', {'followed_links': get_followed_links(owner)})


@login_required
@csrf_exempt
def get_users_followed_links(request):
    return render(request, 'users/links_followed.html', {'followed_links': get_followed_links(get_searcher(request))})

@login_required
@csrf_exempt
def greeting(request):
    greetings = [
        "Hello",
        "Howdy",
        "Hi",
        "Good Day",
        "Sup",
        "Hey",
        "Well hello there",
        "Yo",
        "Greetings"
    ]
    chosen = greetings[random.randint(0, len(greetings)-1)]
    return render(request, 'message.html', {'message': chosen})

@login_required
@csrf_exempt
def username(request):
    return render(request, 'message.html', {'message': request.user.username})
