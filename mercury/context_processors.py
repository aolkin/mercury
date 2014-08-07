
def base(request):
    return { 
        "jsfilename": request.resolver_match.url_name.replace(".views.","/"),
        "viewname": request.resolver_match.url_name.rpartition(".")[2],
    }

def sidebar(request):
    return {}
