from django.db import models
from django.contrib.auth.models import User

class Searcher(models.Model):
    user_profile = models.ForeignKey(User, primary_key=True, unique=True)
