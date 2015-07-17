from django.core.exceptions import ObjectDoesNotExist
from django.db import models

__author__ = 'westonnovelli'

class MainManager(models.Manager):
    """Helper to add new user to their respective group"""
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
