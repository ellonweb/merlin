import Core.db as DB

# This class is based on django.contrib.auth.backends.ModelBackend
# and information in the django docs at this url:
# http://docs.djangoproject.com/en/dev/topics/auth/#writing-an-authentication-backend

class Auth(object):
    def authenticate(self, username=None, password=None):
        print "authing user:", username
        try:
            assert username and password
            return DB.Maps.User.load(name=username, passwd=password)
        except AssertionError as exc:
            # auth middleware only supports TypeError for some reason
            raise TypeError from exc
    def get_user(self, user_id):
        print "get_user id:", user_id
        return DB.Maps.User.load(id=user_id)
    
