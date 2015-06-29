from django.db import models
from django.db.models import Lookup
from openbar.global_util import convert, MainManager
from openbar.global_util import ChoiceEnum
from django.db.models.fields import Field
from openbar_users.models import Searcher
from math import hypot

class ComplexityScore(models.Model):

    def __unicode__(self):
        raise NotImplementedError

    def is_close(self):
        raise NotImplementedError


class BasicComplexityScore(ComplexityScore):
    """
    A Basic Complexity score will be a plotting of average time to master vs. depth of material
    """
    depth_of_material = models.IntegerField()
    average_time_to_master = models.IntegerField()
    radius = 300
    objects = MainManager()

    def __unicode__(self):
        return convert(self.depth_of_material) + str(self.average_time_to_master)

    def is_close(self, other_score):
        dist = self.distance_to(other_score)
        if dist <= self.radius:
            return True, dist
        return False, dist

    def distance_to(self, other_score):
        return hypot(self.average_time_to_master - other_score.average_time_to_master,
                     self.depth_of_material - other_score.depth_of_material)

class Topic(models.Model):
    name = models.CharField(unique=True, max_length=64)
    objects = MainManager()

    def __unicode__(self):
        return self.name


class Medium(ChoiceEnum):
    TEXT = 0
    VIDEO = 1
    SIMULATION = 2
    GAME = 3
    EXERCISES = 4
    OPENSTAX = 5


class Preference(models.Model):
    """
    A Preference is a user's wish to see results that are of X complexity level and in Y mediums, for Topic Z
    """
    topic = models.ForeignKey(Topic)
    medium = models.CharField(max_length=1, choices=Medium.choices())
    complexity_score = models.ForeignKey(ComplexityScore)
    searcher = models.ForeignKey(Searcher)
    objects = MainManager()

    def __unicode__(self):
        medium_text = [choice for choice in Medium.choices() if choice[0] == self.medium][0][1]
        return str(self.topic) + ' ' + medium_text + ' ' + str(self.complexity_score)

class Query(models.Model):
    """
    Query data
    """
    url = models.TextField()        # We may want to consider a max_length parameter here
    media = models.TextField()
    subject = models.TextField()
    title = models.TextField()      # This may change
    complexity_score = models.ForeignKey(ComplexityScore, null=True)
    short_form = models.CharField(max_length=140, default="Preview of the page")
    objects = MainManager()


class Result:
    def __init__(self, query):
        self.query = query
        self.keyword_count = 0
        self.complexity_distance = 0

    def set_keyword_count(self, value):
        self.keyword_count = value
        return self.keyword_count

    def set_complexity_distance(self, value):
        self.complexity_distance = value
        return self.complexity_distance
