__author__ = 'westonnovelli'
from django import forms
from openbar_search.models.results_models import Topic, Medium

class PreferenceForm(forms.Form):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
    medium = forms.TypedChoiceField(Medium.choices(), required=True, coerce=int)
    complexity_score = forms.CharField(required=True)


class SearchForm(forms.Form):
    input = forms.CharField(max_length=256, required=True)
    source = forms.CharField(max_length=32, required=False)
