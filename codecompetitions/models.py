from django.db import models
from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

from django.db.models.signals import *
from django.dispatch import receiver

from django.contrib.auth.models import User, Group

from django.core.files.storage import FileSystemStorage

from django.core.urlresolvers import reverse

from django.conf import settings

from .languages import LANGUAGES

import os, time

class Language(models.Model):
    index = models.PositiveSmallIntegerField(primary_key=True)
    name = CharField(max_length=80,null=True,blank=True,default="Will be auto-populated")
    version = CharField(max_length=160,null=True,blank=True,default="Will be auto-populated")
    custom_help = TextField(null=True,blank=True)

    class Meta:
        ordering = ("index",)

    def __str__(self):
        return self.name

@receiver(pre_save,sender=Language)
def set_language_attributes(sender,instance,*args,**kwargs):
    if instance.index == None:
        instance.index = 0
        while sender.objects.filter(index=instance.index).exists():
            instance.index += 1
        try:
            instance.version = LANGUAGES[instance.index].get_version()
            instance.name = LANGUAGES[instance.index].get_name()
        except IndexError:
            instance.name = "Unknown"
            instance.version = "Undefined Language"

class Competition(models.Model):
    name = CharField(max_length=120)
    description = TextField(null=True,blank=True)

    judges = ManyToManyField(User,related_name="judge_users")
    admins = ManyToManyField(User,related_name="admin_users")
    limit_to = ManyToManyField(Group,blank=True,null=True)
    allowed_languages = ManyToManyField(Language)

    original_time_left = PositiveIntegerField(help_text="in seconds")
    start_time = DateTimeField(blank=True,null=True)
    paused_time_left = PositiveIntegerField(null=True,blank=True,help_text="in seconds")

    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-start_time","-date_modified")

    def get_absolute_url(self):
        return reverse("codecompetitions.views.default",args=(self.id,))

    def __str__(self):
        return self.name

    def languages(self,string=True):
        return ", ".join([i.name for i in self.allowed_languages.all()])

    def get_role(self,user=None):
        if user:
            if self.admins.filter(id=user.id).exists():
                self._cached_role = "admin"
            elif self.judges.filter(id=user.id).exists():
                self._cached_role = "judge"
            else:
                self._cached_role = "compete"
        if not hasattr(self,"_cached_role"):
            raise TypeError("Cache missing and no user supplied!")
        return self._cached_role
            
    def get_admins(self,string=True):
        return (self.admins.all() if not string else 
                ", ".join(["{} {}".format(i.first_name,i.last_name) for i in self.admins.all()]))
    get_admins.short_description = "Admins"

    @property
    def contest_length(self):
        t = time.gmtime(self.original_time_left)
        return time.strftime("%H:%M:%S",t)

    @property
    def remaining_time(self):
        t = time.gmtime(self.paused_time_left if self.paused_time_left else
                        self.original_time_left)
        return time.strftime("%H:%M:%S",t)

class Problem(models.Model):
    name = CharField(max_length=80)
    description = TextField(null=True,blank=True)
    competition = ForeignKey(Competition)

    auto_judge = BooleanField(default=True)
    time_limit = PositiveIntegerField(default=5,help_text="in seconds")
    expected_output = TextField()
    input_data = TextField(null=True,blank=True)
    read_from_file = CharField(max_length=80,null=True,blank=True,
                               help_text="If specified, the input data will be placed into " +
                               "a file with this name in the same directory as the player's " +
                               "code.")

    def __str__(self):
        return self.name

@receiver(pre_save,sender=Problem)
def check_newlines(sender,instance,*args,**kwargs):
    instance.expected_output = instance.expected_output.replace("\r","")
    instance.input_data = instance.input_data.replace("\r","")

run_storage = FileSystemStorage(location=settings.PRIVATE_ROOT,base_url="/private")

def get_run_fn(run,filename):
    return "codecompetitions/c{competition}-p{problem}/{user}/run-{n}/{fn}".format(
        competition = run.problem.competition.id, problem = run.problem.id,
        user = run.user.username, n = run.number, fn = filename)

def get_run_fn_extra(extra,filename):
    return get_run_fn(extra.run,filename)

class Run(models.Model):
    number = PositiveSmallIntegerField()
    problem = ForeignKey(Problem)
    user = ForeignKey(User)
    language = ForeignKey(Language)
    is_a_test = BooleanField(default=False)

    main_file = FileField(upload_to=get_run_fn,max_length=160,storage=run_storage)

    has_been_run = BooleanField(default=False)
    output = TextField(null=True,blank=True)
    runtime = PositiveIntegerField(null=True,blank=True,help_text="in milliseconds")
    exit_code = SmallIntegerField(null=True,blank=True)
    compiled_successfully = NullBooleanField()

    time_to_submission = PositiveIntegerField(null=True,blank=True,help_text="in seconds")
    time_of_submission = DateTimeField(auto_now_add=True)

    judgement = CharField(max_length=120,null=True,blank=True)
    notes = TextField(null=True,blank=True)
    score = PositiveSmallIntegerField(null=True,blank=True)

    @property
    def extra_files(self):
        return [i.file for i in ExtraFile.objects.filter(run=self)]

    def has_extra_files(self):
        return len(self.extra_files) > 0

    def __str__(self):
        return "Run {}".format(self.number)

    def __lt__(self,o):
        return False

class ExtraFile(models.Model):
    file = FileField(upload_to=get_run_fn_extra,max_length=160,storage=run_storage)
    run = ForeignKey(Run)

    def __str__(self):
        return "Extra file '{}' for {}".format(self.file.name.rpartition("/")[2],self.run)
