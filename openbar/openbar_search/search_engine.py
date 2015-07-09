from openbar_search.models.results_models import Query, Result

__author__ = 'westonnovelli'

def complexity_filter(results, user):
    """ Filters to only the results that are within the standard complexity range. """
    for result in results.keys():
        close_enough, radius = result.complexity_score.is_close(user.complexity_score)
        if close_enough:
            results[result].set_complexity_distance(radius)
        else:
            del results[result]

def keyword_filter(results, terms):
    """ Filters to only the results that match the keyword terms. """
    for result in results.keys():
        matches = set(result.title.lower().split(' ')).intersection(set(terms))
        if len(matches) > 0:
            results[result].set_keyword_count(matches)
        else:
            del results[result]

def result_compare(a, b):
    """ Compares two Result objects, returns the best. """
    if a.keyword_count > b.keyword_count or \
       (a.keyword_count == b.keyword_count and not a.complexity_distance > b.complexity_distance):
        return -1
    else:
        return 1

def rank(final_results):
    """ Ranks the results, in this case, basic compare function. """
    results = final_results.values()
    results.sort(result_compare)
    return results

def return_results(search_terms, user):
    raw_results = Query.objects.all()
    final_results = {}
    for result in raw_results:
        final_results[result] = Result(result)
    keyword_filter(final_results, search_terms.lower().split(' '))
    # if user is not None:
        # complexity_filter(final_results, user)
    return rank(final_results)
