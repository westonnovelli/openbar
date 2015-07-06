__author__ = 'westonnovelli'

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import inspect
from enum import Enum


class MainManager(models.Manager):
    """Helper to add new user to their respective group"""
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


def convert(depth_of_material_score, num_to_letter=True):
    """
    Converts the score into the appropriate letter. The scaling of the score corresponds to the constant, the next level
    (which means the next letter) is the next multiple of the constant. For example, if the constant is 38, D, the
    4th letter, would correspond to the 4th multiple of 38... which is 152, so anything less than 152 is a D (or less).

    :param depth_of_material_score: the integer score of the depth of material
    :return: a character corresponding to the score.
    """
    constant = 39
    score_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
                 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
                 23: 'X', 24: 'Y', 25: 'Z', 26: '-'}
    count = 0
    score = constant
    if num_to_letter:
        while score <= depth_of_material_score:
            count += 1
            score += constant
        return score_map[count]
    else:
        return (ord(depth_of_material_score) - ord('A')) * constant

class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices
