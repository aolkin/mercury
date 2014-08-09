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

listeners = ObjectDict()
listeners.competitions = defaultdict(dict)
listeners.problems = defaultdict(dict)

competitions = defaultdict(ObjectDict)

def load_competition(cid):
    if not competitions.get(cid):
        c = Competition.objects.get(pk=cid)
        competitions[c.id].running = False

def update_timers():
    for cid, c in competitions.items():
        if c.running:
            c.time_left = int(c.end_time - time.time())
            if c.time_left < 1:
                c.time_left = 0
                c.running = False
        for i in listeners.competitions[cid].values():
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
            listeners.competitions[self.competition][self.current_user.id] = self
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
                    del listeners.problems[self.problem][self.current_user.id]
                self.problem = obj["problem"]
                self._problem = Problem.objects.get(pk=self.problem)
                listeners.problems[self.problem][self.current_user.id] = self
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
                    if i.mode == "judge":
                        i.write_message({"players": get_players(self.problem)})
            else:
                for i in listeners.problems[self.problem].values():
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
            
            run_user = listeners.competitions[self.competition].get(run.user_id)
            if run_user:
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
            if listeners.problems[self.problem].get(run.user_id):
                listeners.problems[self.problem][run.user_id].write_message({
                    "runs": get_runs_for_player(self.problem,run.user_id)
                })
            data.notify = "Saved judgement for {}'s Run #{}".format(
                get_full_name(run.user), run.number)
            data.notif_title = "Saved Judgement"
            data.notif_type = "info"
            data.icon = "saved"
        if obj.get("request"):
            run = Run.objects.get(pk=obj["request"])
            if self.mode != "compete" and listeners.problems[run.problem_id].get(run.user_id):
                handler = listeners.problems[run.problem_id][run.user_id]
            else:
                handler = self
            runloop.request_run(run, (handler.run_complete,(run,)),
                                4 if self.mode == "compete" else 3)
            data.notify = "Run requested for {}Run #{}.".format(
                (get_full_name(run.user) + "'s " if self.mode != "compete"
                 else ""), run.number)
            data.notif_title = "Run Requested"
            data.notif_type = "info"
            data.icon = "saved"
        if obj.get("clock") and (self._competition.get_role(self.current_user) != "compete"):
            if obj["clock"] == "start":
                competitions[self.competition].end_time = (
                    time.time() + (self._competition.paused_time_left if
                                   self._competition.paused_time_left else
                                   self._competition.original_time_left))
                self._competition.start_time = datetime.datetime.now()
                competitions[self.competition].running = True
            if obj["clock"] == "stop":
                competitions[self.competition].running = False
                self._competition.paused_time_left = competitions[self.competition].time_left
            self._competition.save()

        if len(data) > 0:
            self.write_message(data)

    def run_complete(self,run):
        self.write_message({
            "runs": get_runs_for_player(run.problem_id, run.user_id),
            "notify": "Run #{} was executed {}.".format(
                run.number, "successfully" if run.exit_code == 0 else "unsuccessfully"),
            "notif_type": "success" if run.exit_code == 0 else "danger",
            "notif_title": "Run #{} Execution Complete".format(run.number),
            "link": "#{}-&&{}".format(run.problem_id, run.id),
            "icon": "tasks",
        })
        for i in listeners.problems[run.problem_id].values():
            if i.player == self.current_user.id:
                if run.is_a_test:
                    i.write_message({
                        "runs": get_runs_for_player(run.problem_id, run.user_id),
                    })
                else:
                    i.write_message({
                        "runs": get_runs_for_player(run.problem_id, run.user_id),
                        "notify": "{}'s Run #{} was executed {}.".format(
                            get_full_name(self.current_user), run.number,
                            "successfully" if run.exit_code == 0 else "unsuccessfully"),
                        "notif_type": "success" if run.exit_code == 0 else "danger",
                        "notif_title": "Run #{} Execution Complete".format(run.number),
                        "link": "#{}-&&{}".format(run.problem_id, run.id),
                        "icon": "tasks",
                    })

    def on_close(self):
        try:
            if self.competition:
                del listeners.competitions[self.competition][self.current_user.id]
            if self.problem:
                del listeners.problems[self.problem][self.current_user.id]
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

if settings.DEBUG:
    urls = [
        url(r"/dorun", RequestRunHandler),
        url(r"/", CompetitionHandler),
    ]
else:
    urls = [
        url(r"/", CompetitionHandler),
    ]
