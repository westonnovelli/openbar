__author__ = 'westonnovelli'
from django import forms
from models import Searcher, Folder


class LoginForm(forms.Form):
    name = forms.CharField(label='Name', max_length='25')

class SearcherForm(forms.Form):
    name = forms.CharField(label='Name', max_length='25')

    def __init__(self, *args, **kwargs):
        super(SearcherForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Searcher
        fields = ['name']

class FolderForm(forms.Form):
    title = forms.CharField(label='Title', max_length='256')
