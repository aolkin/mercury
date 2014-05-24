from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from django.http import *

from django.db.models import Q

from django.utils import timezone

from django.contrib import messages

from .models import *

class Done(Exception): pass

def is_accessible(poll,user):
    if poll.restrict_to.count() == 0:
            return True
    for group in poll.restrict_to.all():
        if user.groups.filter(pk=group.pk).exists():
            return True
    return False

def index(request):
    pollset = (Poll.objects.filter(Q(end_date__gt=timezone.now()) |
                                   Q(end_date=None),
                                   enabled=True)
               .prefetch_related("restrict_to")
               .order_by("-end_date","-begin_date"))
    polls = []
    for i in pollset:
        if is_accessible(i,request.user):
            polls.append(i)
    return render(request,"voting/index.html",{"polls":polls})

def vote(request,id_):
    poll = get_object_or_404(Poll,id=id_)
    if not is_accessible(poll,request.user):
        messages.error(request,"You are not allowed to vote in that election!")
        return redirect("voting.views.index")
    questionset = Question.objects.filter(poll=poll).prefetch_related("choices")
    questions = {}
    not_allowed = not poll.allow_edits
    for i in questionset:
        questions[i] = Response.objects.filter(user=request.user,question=i)
        if not questions[i].exists():
            not_allowed = False
    return render(request,"voting/poll.html",locals())

def manage(request,id_):
    return redirect("/admin/")

def new(request):
    return redirect("voting_manage","heh")
