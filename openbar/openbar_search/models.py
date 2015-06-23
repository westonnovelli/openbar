from django.db import models
from openbar.global_util import convert, MainManager
from openbar.global_util import ChoiceEnum
from openbar_users.models import Searcher

class ComplexityScore(models.Model):
    """
    A Complexity score will be a plotting of average time to master vs. depth of material
    """
    depth_of_material = models.IntegerField()
    average_time_to_master = models.IntegerField()
    objects = MainManager()

    def __unicode__(self):
        return convert(self.depth_of_material) + str(self.average_time_to_master)


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
#
# class Query(models.Model):
#     """
#     Query data
#     """
#     url = models.CharField()        # We may want to consider a max_length parameter here
#     media = models.CharField()
#     subject = models.CharField()
#     title = models.CharField()      # This may change
#     objects = MainManager()




