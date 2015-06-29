from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from openbar.global_util import convert

from openbar_search.forms import PreferenceForm, SearchForm
from openbar_search.models import Preference, Medium, ComplexityScore, BasicComplexityScore
from openbar_search.search_engine import return_results
from openbar_users.models import Searcher
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


def search(request):
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
        search_results = return_results(search_form.cleaned_data['input'], request.user)
        return render(request, 'search/results.html', {'results': search_results})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def results(request):
    return render(request, 'search/results.html')
