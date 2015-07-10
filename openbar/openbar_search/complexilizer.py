import random
from openbar.main import index
from openbar_search.models.results_models import Query, BoozeComplexityScore

__author__ = 'westonnovelli'

min = 0
max = 4


def get_random_complexity_score():
    complexity_score, created = BoozeComplexityScore.objects.get_or_create(level=random.randint(min, max))
    return complexity_score

def randomize_complexity(request):
    for query in Query.objects.all():
        complexity_score = get_random_complexity_score()
        query.complexity_score = complexity_score
        query.save()
    return index(request)
