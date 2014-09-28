
from django.conf import settings

from django.utils.safestring import mark_safe

def base(request):
    if request.resolver_match:
        return { 
            "jsfilename": request.resolver_match.url_name.replace(".views.","/"),
            "viewname": request.resolver_match.url_name.rpartition(".")[2],
            "wsaddress": mark_safe(('"ws://"+location.hostname+":5001/{}/"' if settings.DEBUG else
                                    '"ws://"+location.host+"/ws/{}/"').format(
                                        request.resolver_match.url_name.partition(".")[0])),
        }
    else:
        return {}

def sidebar(request):
    return {}
