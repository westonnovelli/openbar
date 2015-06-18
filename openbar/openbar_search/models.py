from django.db import models
from openbar.global_util import convert
from openbar_users.models import Searcher

class ComplexityScore(models.Model):
    """
    A Complexity score will be a plotting of average time to master vs. depth of material
    """
    depth_of_material = models.IntegerField()
    average_time_to_master = models.IntegerField()

    def __unicode__(self):
        return convert(self.depth_of_material)+'-'+str(self.average_time_to_master)


class Preference(models.Model):
    """
    A Preference is a user's wish to see results that are of X complexity level and in Y mediums
    """
    VIDEO = 'V'
    SIMULATION = 'S'
    GAME = 'G'
    TEXT = 'T'
    OPENSTAX = 'O'
    MEDIUM_CHOICES = ((VIDEO, 'video'),
                      (SIMULATION, 'simulation'),
                      (GAME, 'game'),
                      (TEXT, 'text'),
                      (OPENSTAX, 'openstax'))
    medium = models.CharField(max_length=2, choices=MEDIUM_CHOICES, default='T')
    topic = models.IntegerField()
    complexity_score = models.ForeignKey(ComplexityScore)
    searcher = models.ForeignKey(Searcher)
