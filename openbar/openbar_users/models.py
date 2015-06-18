from django.db import models
from django.contrib.auth.models import User
from openbar_search.models import ComplexityScore, Preference

class Searcher(models.Model):
    user_profile = models.ForeignKey(User)
    complexity_score = models.ForeignKey(ComplexityScore)
    search_preferences = models.ForeignKey(Preference)
