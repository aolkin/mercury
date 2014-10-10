from tornado.web import url, RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.ioloop import IOLoop
from tornado.util import ObjectDict

from collections import defaultdict
from json import loads

import time, os, datetime

from tornado_support.handlers import DjangoUserMixin

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
User = get_user_model()

from .runthread import RunLoop

from .models import *

def get_full_name(user):
    return user.first_name + " " + user.last_name

runloop = RunLoop()
runloop.start()

defaultdict_list = lambda: defaultdict(list)

listeners = ObjectDict()
listeners.competitions = defaultdict(defaultdict_list)
listeners.problems = defaultdict(defaultdict_list)
listeners.scoreboards = defaultdict(list)

competitions = defaultdict(ObjectDict)
competition_scores = defaultdict(ObjectDict)

def load_competition(cid):
    if not competitions.get(cid):
        c = Competition.objects.get(pk=cid)
        if c.start_time:
            competitions[cid].running = True
            competitions[cid].end_time = ((c.start_time + datetime.timedelta(
                seconds = c.paused_time_left if c.paused_time_left else c.original_time_left))
                                          .timestamp())
        else:
            competitions[cid].running = False
        IOLoop.current().add_callback(load_competition_scores,cid)
    else:
        return True

def send_scores(cid):
    scores = sorted([i for i in competition_scores[cid].scores.values()],
                    key=lambda x: (x.total_score if hasattr(x,"total_score") else
                                   (x.score if hasattr(x,"score") else 0)), reverse=True)
    for i in listeners.scoreboards[cid]:
        if settings.DEBUG:
            print("Sending scores:",scores)
        i.write_message({
            "scores": scores,
            "debug": settings.DEBUG
        })

def update_score(u,cid,initial=False):
    c = competition_scores[cid]
    c.scores[u].player = get_full_name(User.objects.get(id=u))
    c.scores[u].cid = cid
    if cid == "global":
        for i in c.problems:
            load_competition_scores(i)
        runs = [competition_scores[i].scores[u] for i in competition_scores
                if (i != "global" and competition_scores[i].scores[u].get("cid"))]
    else:
        runs = [Run.objects.filter(user=u, problem=p,
                                   score__isnull=False,
                                   is_a_test=False).order_by("-number")[0]
                for p in Run.objects.filter(
                        is_a_test=False, problem__competition=cid, user=u,
                        score__isnull=False).distinct().values_list("problem",flat=True)]
    c.scores[u].total_score = sum([i.score if hasattr(i,"score") else i.total_score for i in runs])
    if cid == "global":
        total = len([i for i in runs if i.get("cid")])
    else:
        total = len(runs)
    c.scores[u].average_score = round(c.scores[u].total_score / total, 2)
    c.scores[u].problems = defaultdict(ObjectDict)
    for run in runs:
        if cid == "global":
            c.scores[u].problems[c.problems.index(run.cid)].score = run.total_score
        else:
            c.scores[u].problems[c.problems.index(run.problem_id)].score = run.score
    if not initial:
        send_scores(cid)

def load_competition_scores(cid):
    c = competition_scores[cid]
    c.scores = defaultdict(ObjectDict)
    if cid == "global":
        c.problems = list(Competition.objects.all().order_by("id").values_list("id",flat=True))
        runset = Run.objects.filter(is_a_test=False)
    else:
        c.problems = list(Problem.objects.filter(competition=cid).order_by("id")
                          .values_list("id",flat=True))
        runset = Run.objects.filter(problem__competition=cid, is_a_test=False)
    for u in runset.distinct().values_list("user",flat=True):
        update_score(u,cid,True)
    send_scores(cid)

def update_timers():
    for cid, c in competitions.items():
        if c.running:
            c.time_left = int(c.end_time - time.time())
            if c.time_left < 1:
                c.time_left = 0
                c.running = False
                competition = Competition.objects.get(pk=cid)
                competition.paused_time_left = 0
                competition.save()
        for i in [i for l in listeners.competitions[cid].values() for i in l]:
            try:
                i.write_message(c)
            except WebSocketClosedError:
                pass
    IOLoop.current().call_later(1,update_timers)

IOLoop.current().call_later(1,update_timers)

def competition_clock_operation(op,c):
    if op == "start":
        c = Competition.objects.get(pk=c.id)
        competitions[c.id].end_time = (
            time.time() + (c.paused_time_left if
                           c.paused_time_left else
                           c.original_time_left))
        c.start_time = datetime.datetime.now(datetime.timezone.utc)
        competitions[c.id].running = True
    if op == "stop":
        competitions[c.id].running = False
        c.paused_time_left = competitions[c.id].time_left
        c.start_time = None
    c.save()

def get_players(problem):
    players = Run.objects.filter(problem=problem).distinct().values_list("user",flat=True)
    users = [User.objects.filter(pk=i) for i in players]
    return [i.values("first_name","last_name","id")[0] for i in users]

def get_runs_for_player(problem,user):
    runs = Run.objects.filter(problem=problem, user=user).values(
        "id", "number", "language", "is_a_test", "has_been_run",
        "output", "runtime", "exit_code", "compiled_successfully",
        "time_to_submission", "judgement", "notes", "score")
    runlist = []
    for i in runs:
        run = Run.objects.get(pk=i["id"])
        i["language"] = run.language.version
        try:
            contents = run.main_file.read().decode().strip()
        except UnicodeDecodeError as err:
            contents = "Binary File"
        i["main_file"] = {"name": os.path.basename(run.main_file.name),
                          "contents": contents}
        i["extra_files"] = []
        for f in run.extra_files:
            try:
                contents = f.read().decode().strip()
            except UnicodeDecodeError as err:
                contents = "Binary File"
            i["extra_files"].append({"name": os.path.basename(f.name),
                                     "contents": contents})
        runlist.append(i)
    return runlist

class CompetitionHandler(DjangoUserMixin,WebSocketHandler):
    def open(self):
        self.get_current_user()
        self.competition = None
        self.problem = None
        self.player = None
        self.mode = "compete"

    def on_message(self,message):
        if not self.current_user.is_authenticated():
            self.write_message({"error": "logged_out"})
            return False

        obj = loads(message)
        data = ObjectDict()

        if settings.DEBUG:
            print(obj)
            data.debug = True

        if obj.get("echo"):
            data.echo = obj["echo"]
        
        if obj.get("competition"):
            self.competition = obj["competition"]
            self._competition = Competition.objects.get(pk=self.competition)
            listeners.competitions[self.competition][self.current_user.id].append(self)
            load_competition(self.competition)
        
        if obj.get("mode"):
            if (obj["mode"] != "compete" and
                self._competition.get_role(self.current_user) == "compete"):
                data.error = "Unauthorized mode"
            else:
                self.mode = obj["mode"]
        
        if obj.get("problem"):
            if obj["problem"] != self.problem:
                if self.problem:
                    listeners.problems[self.problem][self.current_user.id].remove(self)
                self.problem = obj["problem"]
                self._problem = Problem.objects.get(pk=self.problem)
                listeners.problems[self.problem][self.current_user.id].append(self)
            data.problem_name = self._problem.name
            data.description = self._problem.description
            if self.mode == "compete":
                data.runs = get_runs_for_player(self.problem,self.current_user.id)
            elif self._competition.get_role(self.current_user) != "compete":
                data.expected_output = self._problem.expected_output
                data.players = get_players(self.problem)
        
        if obj.get("player") and self._competition.get_role(self.current_user) != "compete":
            if obj["player"] != self.player:
                self.player = int(obj["player"])
                data.runs = get_runs_for_player(self.problem,self.player)
        
        if obj.get("main_file"):
            last_run = Run.objects.filter(user=self.current_user.id,
                                          problem=self.problem).order_by("-number")
            if last_run.exists():
                number = last_run.values_list("number",flat=True)[0] + 1
            else:
                number = 1
            run = Run(number=number, problem_id=self.problem, user=self.current_user,
                      language_id=obj["language"], is_a_test=obj["test_run"],
                      time_to_submission=(self._competition.original_time_left -
                                          (competitions[self._competition.id].end_time -
                                           time.time())), runtime=None)
            run.main_file.save(obj["main_file"]["name"],
                               ContentFile(obj["main_file"]["contents"].replace("\r","")))
            for i in obj["extra_files"]:
                extra_file = ExtraFile(run=run)
                extra_file.file.save(i["name"],
                                     ContentFile(i["contents"].replace("\r","")))
            data.upload = {"id": run.id, "number": run.number}
            data.runs = get_runs_for_player(self.problem,self.current_user.id)

            if len(data.runs) == 1:
                for i in listeners.problems[self.problem].values():
                    for j in [j for j in i if j.mode == "judge"]:
                        j.write_message({"players": get_players(self.problem)})
            else:
                for i in [i for l in listeners.problems[self.problem].values() for i in l]:
                    if i.player == self.current_user.id:
                        if run.is_a_test:
                            i.write_message({
                                "runs": data.runs,
                            })
                        else:
                            i.write_message({
                                "runs": data.runs,
                                "notify": "{} uploaded Run #{}".format(
                                    get_full_name(self.current_user), run.number),
                                "notif_type": "info",
                                "icon": "send",
                            })
            runloop.request_run(run,(self.run_complete,(run,)))
        
        if obj.get("judgement"):
            run = Run.objects.get(pk=obj["run"])
            run.judgement = obj["judgement"]
            run.score = obj["score"]
            run.notes = obj["notes"]
            run.save()
            update_score(run.user_id,self.competition)
            
            run_users = [i for i in listeners.competitions[self.competition].get(run.user_id,[])
                         if (hasattr(i,"mode") and i.mode == "compete")]
            for run_user in run_users:
                if run_user.problem == run.problem_id:
                    problem_text = ""
                else:
                    problem_text = " of problem {}".format(run.problem.name)
                run_user.write_message({
                    "notify": "Run #{}{} was judged '{}' with a score of {} by {}".format(
                        run.number, problem_text, run.judgement, run.score,
                        get_full_name(self.current_user)),
                    "notif_title": "Judgement for Run #{}{}".format(run.number, problem_text),
                    "notif_type": "success" if run.judgement == "Correct" else "danger",
                    "link": "#{}-&&{}".format(run.problem_id, run.id),
                    "icon": "star",
                })
            for listener in listeners.problems[self.problem].get(run.user_id,[]):
                listener.write_message({
                    "runs": get_runs_for_player(self.problem,run.user_id)
                })
            data.notify = "Saved judgement for {}'s Run #{}".format(
                get_full_name(run.user), run.number)
            data.notif_title = "Saved Judgement"
            data.notif_type = "info"
            data.icon = "saved"
        
        if obj.get("request"):
            run = Run.objects.get(pk=obj["request"])
            players = [i for i in listeners.problems[run.problem_id]
                       .get(run.user_id,[]) if i.mode == "compete"]
            if self.mode != "compete" and len(players) > 0:
                handlers = players
            else:
                handlers = [self]
            runloop.request_run(run, ((lambda handlers, run, u:
                                       [handler.run_complete(run, u) for handler in handlers]),
                                      (handlers, run, get_full_name(self.current_user))),
                                4 if self.mode == "compete" else 3)
            data.notify = "Run requested for {}Run #{}.".format(
                (get_full_name(run.user) + "'s " if self.mode != "compete"
                 else ""), run.number)
            data.notif_title = "Run Requested"
            data.notif_type = "info"
            data.icon = "saved"
        
        if obj.get("clock") and (self._competition.get_role(self.current_user) != "compete"):
            competition_clock_operation(obj["clock"],self._competition)

        if len(data) > 0:
            try:
                self.write_message(data)
            except WebSocketClosedError:
                pass

    def run_complete(self,run,requester=False):
        if (not run.is_a_test) and run.score != None:
            IOLoop.current().add_callback(update_score, run.user_id, run.problem.competition_id)
        if self.mode == "compete":
            if requester:
                message = "Execution of Run #{} (requested by {}) was completed {}.".format(
                    run.number, requester,
                    "successfully" if run.exit_code == 0 else "unsuccessfully")
            else:
                message = "Run #{} was executed {}.".format(
                    run.number, "successfully" if run.exit_code == 0 else "unsuccessfully")
            self.write_message({
                "runs": get_runs_for_player(run.problem_id, run.user_id),
                "notify": message,
                "notif_type": "success" if run.exit_code == 0 else "danger",
                "notif_title": "Run #{} Execution Complete".format(run.number),
                "link": "#{}-&&{}".format(run.problem_id, run.id),
                "icon": "tasks",
            })
        if requester:
            message = "Execution of {}'s Run #{} (requested by {}) was completed {}.".format(
                get_full_name(self.current_user), run.number, requester,
                "successfully" if run.exit_code == 0 else "unsuccessfully")
        else:
            message = "{}'s Run #{} was executed {}.".format(
                get_full_name(self.current_user), run.number,
                "successfully" if run.exit_code == 0 else "unsuccessfully")
        for i in [i for l in listeners.problems[run.problem_id].values() for i in l]:
            if i.player == self.current_user.id:
                if (not requester) and run.is_a_test:
                    i.write_message({
                        "runs": get_runs_for_player(run.problem_id, run.user_id),
                    })
                else:
                    i.write_message({
                        "runs": get_runs_for_player(run.problem_id, run.user_id),
                        "notify": message,
                        "notif_type": "success" if run.exit_code == 0 else "danger",
                        "notif_title": "Run #{} Execution Complete".format(run.number),
                        "link": "#{}-&&{}".format(run.problem_id, run.id),
                        "icon": "tasks",
                    })

    def on_close(self):
        try:
            if hasattr(self,"_competition"):
                listeners.competitions[self.competition][self.current_user.id].remove(self)
            if hasattr(self,"_problem"):
                listeners.problems[self.problem][self.current_user.id].remove(self)
        except ValueError:
            pass
        
    def check_origin(self,origin):
        return True
        if settings.DEBUG:
            return True
        else:
            return super().check_origin(origin)

class ScoreboardHandler(DjangoUserMixin,WebSocketHandler):
    def open(self):
        self.get_current_user()
        self.competition = None

    def on_message(self,message):
        if not self.current_user.is_authenticated():
            self.write_message({"error": "logged_out"})
            return False

        obj = loads(message)
        data = ObjectDict()

        if settings.DEBUG:
            print(obj)
            data.debug = True
        
        if obj.get("competition"):
            if obj["competition"] == "global":
                self.competition = "global"
                IOLoop.current().add_callback(load_competition_scores,self.competition)
            else:
                self.competition = obj["competition"]
                self._competition = Competition.objects.get(pk=self.competition)
                listeners.competitions[self.competition][self.current_user.id].append(self)
                if load_competition(self.competition):
                    IOLoop.current().add_callback(send_scores,self.competition)
            listeners.scoreboards[self.competition].append(self)
        
        if obj.get("clock") and (self._competition.get_role(self.current_user) != "compete"):
            competition_clock_operation(obj["clock"],self._competition)

        self.write_message(data)

    def on_close(self):
        try:
            if hasattr(self,"competition"):
                listeners.scoreboards[self.competition].remove(self)
                listeners.competitions[self.competition][self.current_user.id].remove(self)
        except ValueError:
            pass        
        
    def check_origin(self,origin):
        return True
        if settings.DEBUG:
            return True
        else:
            return super().check_origin(origin)

class RequestRunHandler(RequestHandler):
    def get(self):
        runs = Run.objects.filter(has_been_run=False)
        if runs.exists():
            runloop.request_run(runs[0])
            self.write("Run requested")
        else:
            self.write("Nothing to run")

URLS = [
        url(r"/scoreboard/", ScoreboardHandler),
        url(r"/", CompetitionHandler),
]

if settings.DEBUG:
    urls = [
        url(r"/dorun", RequestRunHandler),
    ] + URLS
else:
    urls = URLS
