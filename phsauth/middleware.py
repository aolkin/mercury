from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

class RequireLoginMiddleware:
    def __init__(self):
        self.require_login_path = reverse(settings.LOGIN_URL)
    
    def process_request(self, request):
        if request.path != self.require_login_path and request.user.is_anonymous():
            if request.is_ajax():
                return JsonResponse({"success": False, "logged_out": True,
                                     "error": "You have been logged out.",})
            return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
