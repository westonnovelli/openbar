from django.contrib import admin as django_admin
from openbar_users import models

# Register your models here.
django_admin.site.register(models.Searcher)
django_admin.site.register(models.Folder)
