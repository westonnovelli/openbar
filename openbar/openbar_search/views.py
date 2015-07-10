from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from openbar.global_util import convert
import random

from openbar_search.forms import PreferenceForm, SearchForm
from openbar_search.models.results_models import Preference, Medium, BasicComplexityScore, Query
from openbar_search.search_engine import return_results
from openbar_users.forms import LoginForm
from openbar_users.models import Searcher, Folder
from openbar_users.views import home_view


@login_required
def add_preference(request):
    preference_form = PreferenceForm(request.POST or None)
    if preference_form.is_valid():
        topic = preference_form.cleaned_data['topic']
        medium = int(preference_form.cleaned_data['medium'])
        complexity_score = preference_form.cleaned_data['complexity_score']
        x_axis = complexity_score[0]
        y_axis = complexity_score[1:]

        medium_obj = Medium.choices()[medium][0]
        complexity_score_obj, created = BasicComplexityScore.objects.get_or_create(depth_of_material=convert(x_axis, False),
                                                                                   average_time_to_master=y_axis)
        searcher_obj = Searcher.objects.get_or_none(user_profile=request.user)
        new_preference = Preference(topic=topic,
                                    medium=medium_obj,
                                    complexity_score=complexity_score_obj,
                                    searcher=searcher_obj)
        new_preference.save()
    return redirect(home_view)

@csrf_exempt
def search(request):
    if request.POST:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():

            search_results = return_results(search_form.cleaned_data['input'], request.user)
            data = {'results': search_results}
            if search_form.cleaned_data['source'] == "extension":
                return render(request, 'search/results_extension.html', data)
            return render(request, 'search/results.html', data)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def results(request):
    return render(request, 'search/results.html')


def increase_complexity_score(request):
    query = Query.objects.get_or_none(id=request.GET['id'])
    if query is not None:
        val = int(request.GET['amount'])
        score = query.complexity_score
        for i in range(val):
            score.increase_complexity_score()
        score.save()
        query.save()
        return render(request, 'message.html', {'message': score.show()})
    return render(request, 'index.html', {'login_form': LoginForm()})


def decrease_complexity_score(request):
    query = Query.objects.get_or_none(id=request.GET['id'])
    if query is not None:
        val = int(request.GET['amount'])
        score = query.complexity_score
        for i in range(val):
            score.decrease_complexity_score()
        score.save()
        query.save()
        return render(request, 'message.html', {'message': score.show()})
    return render(request, 'index.html', {'login_form': LoginForm()})

def set_complexity_score(request):
    query = Query.objects.get_or_none(id=request.GET['id'])
    if query is not None:
        other = Query.objects.get_or_none(id=request.GET['amount'])
        score = query.complexity_score
        if other is not None:
            score.set_complexity_score(other.complexity_score)
        score.save()
        query.save()
        return render(request, 'message.html', {'message': score.show()})
    return render(request, 'index.html', {'login_form': LoginForm()})


def get_random_query(request=None):
    randomQ = None
    if request is not None and request.GET["id"] != "":
        randomQ = Query.objects.get_or_none(id=request.GET["id"])
    while randomQ is None:
        random_id = random.randint(5, 10000)
        randomQ = Query.objects.get_or_none(id=random_id)
    if request is not None:
        return render(request, 'search/new_random.html', {'query': randomQ})
    return randomQ

def normalize_scores(request):
    data = {'first': get_random_query()}
    data['second'] = get_random_query()
    return render(request, 'search/normalize_score.html', data)

def extension(request):
    return render(request, 'search/extension_page.html')
