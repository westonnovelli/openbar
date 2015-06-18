from django.shortcuts import render

__author__ = 'westonnovelli'

def index(request):
    """Render root landing page from template"""
    return render(request, 'index.html')
