from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import *
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

from .models import *

from .votecounters import COUNTING_METHODS

import json

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
            i.user_allowed(request.user,True)
    adminpolls = Poll.objects.filter(admins=request.user)
    return render(request,"voting/index.html",{"polls":polls,"adminpolls":adminpolls})

class VotingNotAllowedError(Exception): pass

def vote(request,id_):
    poll = get_object_or_404(Poll,id=id_)
    try:
        if not is_accessible(poll,request.user):
            raise VotingNotAllowedError("You are not allowed to vote in {} poll!")
        if not poll.enabled:
            raise VotingNotAllowedError("{} poll is not available.")
        if poll.end_date < timezone.now():
            raise VotingNotAllowedError("{} poll has been closed.")
        if poll.begin_date > timezone.now():
            raise VotingNotAllowedError("{} poll is not open yet.")
        if not poll.user_allowed(request.user):
            raise VotingNotAllowedError("You have already submitted your vote and you may not change it.")
    except VotingNotAllowedError as err:
        if request.is_ajax():
            return JsonResponse({"success": False, 
                                 "error": err.args[0].format("this").capitalize()})
        else:
            messages.error(request,err.args[0].format("that").capitalize())
            return redirect("voting.views.index")

    ### Perform save
    if request.method == "POST" and request.is_ajax():
        for question, res in json.loads(request.POST["data"]).items():
            for i, choice in res.items():
                obj, created = Response.objects.get_or_create(user=request.user,
                                                              question_id=int(question),
                                                              choice_extra=i)
                obj.choice_id = choice
                obj.save()
        messages.success(request,'Thanks for voting! Don\'t forget to <a href="{}">log out</a> when you are done.'.format(reverse("logout")),extra_tags="html-safe")
        return JsonResponse({"success":True,"redirect":reverse(index)})

    ### Display poll
    questionset = Question.objects.filter(poll=poll).prefetch_related("choices")
    questions = {}
    not_allowed = not poll.allow_edits
    for i in questionset:
        questions[i] = Response.objects.filter(user=request.user,question=i)
        if not questions[i].exists():
            not_allowed = False
    return render(request,"voting/poll.html",locals())

def manage(request,id_):
    poll = get_object_or_404(Poll,id=id_)
    return render(request,"voting/manage.html",locals())

def get_results(request,id_):
    poll = get_object_or_404(Poll,id=id_)
    results = {}
    for question in poll.question_set.all():
        method = COUNTING_METHODS[question.kind]
        results[question.name] = {}
        responseset = Response.objects.filter(question=question).order_by("user","choice_extra")
        responses = []
        user = None
        res = None
        for i in responseset:
            if i.user != user:
                user = i.user
                if res:
                    responses.append(method.response_type(*res))
                res = []
            res.append(i.choice.name)
        responses.append(method.response_type(*res))
        counter = method(responses)
        steps = []
        for i in counter:
            steps.append(i)
        results[question.name] = [counter.get(),steps]
    return JsonResponse(results)

def new(request):
    return redirect("voting_manage","heh")
