from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from openbar.global_util import convert

from openbar_search.forms import PreferenceForm
from openbar_search.models import Preference, Topic, Medium, ComplexityScore
from openbar_users.models import Searcher
from openbar_users.views import home_view


@login_required
def add_preference(request):
    preference_form = PreferenceForm(request.POST or None)
    if preference_form.is_valid():
        print "got valid request"
        topic = preference_form.cleaned_data['topic']
        medium = int(preference_form.cleaned_data['medium'])
        complexity_score = preference_form.cleaned_data['complexity_score']
        x_axis = complexity_score[0]
        y_axis = complexity_score[1:]

        medium_obj = Medium.choices()[medium][0]
        complexity_score_obj, created = ComplexityScore.objects.get_or_create(depth_of_material=convert(x_axis, False),
                                                                              average_time_to_master=y_axis)
        searcher_obj = Searcher.objects.get_or_none(user_profile=request.user)
        new_preference = Preference(topic=topic,
                                    medium=medium_obj,
                                    complexity_score=complexity_score_obj,
                                    searcher=searcher_obj)
        new_preference.save()
    return redirect(home_view)
