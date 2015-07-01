import random
from openbar.main import index
from openbar_search.models import Query, BasicComplexityScore

__author__ = 'westonnovelli'

min = 0
max = 1000



def get_random_complexity_score():
    complexity_score = BasicComplexityScore(depth_of_material=random.randint(min, max),
                                            average_time_to_master=random.randint(min, max))
    complexity_score.save()
    return complexity_score

def randomize_complexity(request):
    for query in Query.objects.all():
        complexity_score = get_random_complexity_score()
        query.complexity_score = complexity_score
        query.save()
    return index(request)