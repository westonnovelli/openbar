__author__ = 'westonnovelli'

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class MainManager(models.Manager):
    """Helper to add new user to their respective group"""
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


def convert(depth_of_material_score):
    """
    Converts the score into the appropriate letter. The scaling of the score corresponds to the constant, the next level
    (which means the next letter) is the next multiple of the constant. For example, if the constant is 38, D, the
    4th letter, would correspond to the 4th multiple of 38... which is 152, so anything less than 152 is a D (or less).

    :param depth_of_material_score: the integer score of the depth of material
    :return: a character corresponding to the score.
    """
    constant = 38
    score_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
                 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W',
                 24: 'X', 25: 'Y', 26: 'Z'}
    count = 0
    score = 0
    while score < depth_of_material_score:
        count += 1
        score += constant
    return score_map[count]
