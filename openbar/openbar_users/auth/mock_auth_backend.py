__author__ = 'westonnovelli'

from django.contrib.auth.models import User


class MockAuthBackend(object):
    """
    Mock backend for authenticating users
    """

    def authenticate(self, username=None, password=None):
        """
        Will return user object if user with the supplied username exists,
        otherwise will return None

        :param username: Supplied username of user
        :param password: Not used, but required
        :return: User if exists, null otherwise
        """
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None