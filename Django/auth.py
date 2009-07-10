import Core.db as DB

# Code based on information from the django docs on middleware:
# http://docs.djangoproject.com/en/dev/topics/http/middleware/
# class Session based on django.contrib.sessions.middleware.SessionMiddleware
# class Auth based on django.contrib.auth.middleware.AuthMiddleware

class Session(object):
    pass

class Auth(object):
    pass
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
    
