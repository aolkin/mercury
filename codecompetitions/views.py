from django.shortcuts import render, redirect

from django.contrib import messages

from .models import *

def is_accessible(competition,user):
    if competition.limit_to.count() == 0:
        return True
    for group in competition.limit_to.all():
        if user.groups.filter(pk=group.pk).exists():
            return True
    return False

def index(request):
    competitionset = (Competition.objects.all()
                      .prefetch_related("limit_to")[:10])
    competitions = []
    for i in competitionset:
        if (i.get_role(request.user) in ("admin","judge")) or is_accessible(i,request.user):
            competitions.append(i)
    return render(request, "codecompetitions/index.html", {"competitions": competitions,
                                                           "admin": request.user.is_staff})

def compete(request,cid):
    c = Competition.objects.get(id=cid)
    c.get_role(request.user)
    languages = c.allowed_languages.all()
    return render(request, "codecompetitions/competition.html",
                  {"c": c, "langs": languages})

def judge(request,cid):
    c = Competition.objects.get(id=cid)
    if not (c.get_role(request.user) in ("admin","judge")):
        messages.add_message(request, messages.ERROR,
                             "You are not allowed to judge '{}'.".format(c.name))
        return redirect(default,cid)
    return render(request, "codecompetitions/competition.html", {"c":c})

def admin(request,cid):
    c = Competition.objects.get(id=cid)
    if c.get_role(request.user) != "admin":
        messages.add_message(request, messages.ERROR,
                             "You are not allowed to administrate '{}'.".format(c.name))
        return redirect(default,cid)
    return redirect("admin:codecompetitions_competition_change",cid)
    return render(request, "codecompetitions/competition.html", {"c":c})

def default(request,cid):
    c = Competition.objects.get(id=cid)
    return redirect("codecompetitions.views."+c.get_role(request.user),cid)

def scoreboard(request,cid=None):
    if cid:
        c = Competition.objects.get(id=cid)
        c.get_role(request.user)
        fields = Problem.objects.filter(
            competition=c).order_by("id").values_list("name",flat=True)
    else:
        c = None
        fields = Competition.objects.all().order_by("id").values_list("name",flat=True)
    popup = bool(request.GET.get("popup"))
    return render(request, "codecompetitions/score.html",
                  {"c": c, "popup": popup, "fields": fields})
