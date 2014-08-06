import django

class DjangoUserMixin():
    def __init__(self,*args,**kwargs):
        pass
        
    def get_django_session(self):
        if not hasattr(self, 'session'):
            engine = django.utils.importlib.import_module(
                django.conf.settings.SESSION_ENGINE)
            session_key = self.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)
            self.session = engine.SessionStore(session_key)
        return self.session
 
    def get_current_user(self):
        # get_user needs a django request object, but only looks at the session
        self.get_django_session()
        self.current_user = django.contrib.auth.get_user(self)
        return self.current_user
 
    def get_django_request(self):
        request = django.core.handlers.wsgi.WSGIRequest(
            tornado.wsgi.WSGIContainer.environ(self.request))
        request.session = self.get_django_session()
        
        if self.current_user:
            request.user = self.current_user
        else:
            request.user = django.contrib.auth.models.AnonymousUser() 
        return request
