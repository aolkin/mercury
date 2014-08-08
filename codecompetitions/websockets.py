from tornado.web import url, RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.ioloop import IOLoop
from tornado.util import ObjectDict

from collections import defaultdict
from json import loads

import time, os

from tornado_support.handlers import DjangoUserMixin

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
User = get_user_model()

from .runthread import RunLoop
# runloop.request_run(run,callback=None,priority=5)

from .models import *

runloop = RunLoop()
runloop.start()

listeners = ObjectDict()
listeners.competitions = defaultdict(list)
listeners.problems = defaultdict(list)

competitions = defaultdict(ObjectDict)

def load_competition(cid):
    ### Fix this once start and stop are implemented
    if not competitions.get(cid):
        c = Competition.objects.get(pk=cid)
        competitions[c.id].running = True
        competitions[c.id].time_left = c.original_time_left
        competitions[c.id].end_time = time.time() + c.original_time_left

def update_timers():
    for cid, c in competitions.items():
        if c.running:
            c.time_left = int(c.end_time - time.time())
            if c.time_left < 1:
                c.time_left = 0
                c.running = False
        for i in listeners.competitions[cid]:
            try:
                i.write_message(c)
            except WebSocketClosedError:
                pass
    IOLoop.current().call_later(1,update_timers)

IOLoop.current().call_later(1,update_timers)

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
        i["main_file"] = {"name": os.path.basename(run.main_file.name),
                          "contents": run.main_file.read().decode().strip()}
        i["extra_files"] = []
        for f in run.extra_files:
            i["extra_files"].append({"name": os.path.basename(f.name),
                                     "contents": f.read().decode().strip()})
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
        obj = loads(message)
        data = ObjectDict()

        if settings.DEBUG:
            print(obj)
            data.debug = True

        if obj.get("mode"):
            self.mode = obj["mode"]
        if obj.get("competition"):
            self.competition = obj["competition"]
            self._competition = Competition.objects.get(pk=self.competition)
            listeners.competitions[self.competition].append(self)
            load_competition(self.competition)
        if obj.get("problem"):
            if obj["problem"] != self.problem:
                if self.problem:
                    listeners.problems[self.problem].remove(self)
                self.problem = obj["problem"]
                self._problem = Problem.objects.get(pk=self.problem)
                listeners.problems[self.problem].append(self)
            data.description = self._problem.description
            if self.mode == "compete":
                data.runs = get_runs_for_player(self.problem,self.current_user.id)
            elif self._competition.get_role(self.current_user) != "compete":
                data.expected_output = self._problem.expected_output
                data.players = get_players(self.problem)
        if obj.get("player") and self._competition.get_role(self.current_user) != "compete":
            if obj["player"] != self.player:
                self.player = obj["player"]
                data.runs = get_runs_for_player(self.problem,self.player)
        if len(data) > 0:
            self.write_message(data)

    def on_close(self):
        try:
            if self.competition:
                listeners.competitions[self.competition].remove(self)
            if self.problem:
                listeners.problems[self.problem].remove(self)
        except ValueError:
            pass
        
    def check_origin(self,origin):
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

urls = [
    url(r"/dorun", RequestRunHandler),
    url(r"/", CompetitionHandler),
]
