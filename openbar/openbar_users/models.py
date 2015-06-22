from django.db import models
from django.contrib.auth.models import User
from openbar.global_util import MainManager

user_manager = MainManager()
user_manager.contribute_to_class(User, 'custom_objects')


class Searcher(models.Model):
    user_profile = models.OneToOneField(User, primary_key=True)
    objects = MainManager()
