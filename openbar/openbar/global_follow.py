from openbar_users.models import FollowedLink

__author__ = 'westonnovelli'

def latest_first(a, b):
    """ Compares two FollowedLink objects, returns the most recently followed link. """
    if a.date_followed < b.date_followed:
        return -1
    else:
        return 1

def get_followed_links(searcher):
    followed_links = FollowedLink.objects.filter(owner=searcher).order_by('-date_followed')[:5]
    return followed_links

