from django.contrib import admin as django_admin
from openbar_search import models

# Register your models here.
django_admin.site.register(models.BasicComplexityScore)
django_admin.site.register(models.Preference)
