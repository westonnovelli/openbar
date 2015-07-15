from django.db import models
from django.contrib.auth.models import User
from openbar.global_util import MainManager
from openbar_search.models.results_models import BoozeComplexityScore, Query

user_manager = MainManager()
user_manager.contribute_to_class(User, 'custom_objects')


class Searcher(models.Model):
    user_profile = models.OneToOneField(User, primary_key=True)
    complexity_score = models.ForeignKey(BoozeComplexityScore, null=True)
    objects = MainManager()


class Folder(models.Model):
    title = models.CharField(max_length=256)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    items = models.ManyToManyField(Query)
    owner = models.ForeignKey(Searcher)
    objects = MainManager()
