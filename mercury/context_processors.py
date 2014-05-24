
def base(request):
    return { 
        "jsfilename": request.resolver_match.url_name.replace(".views.","/")
    }

def sidebar(request):
    return {}
