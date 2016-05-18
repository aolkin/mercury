from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group

from django.utils.html import format_html
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class VoteObject(models.Model):
    name = models.CharField(max_length=80)
    desc = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="voting_images/%Y-%m/",blank=True,null=True)

    def __str__(self):
        return self.name

    def _imghtml(self,w=48,h=48):
        if self.image:
            return format_html('<img src="{0}" height="{1}" width="{2}" />',
                               self.image.url,min(w,self.image.width),min(h,self.image.height))
        else:
            return ''
    _imghtml.allow_tags = True
    _imghtml.short_description = "Image"

    class Meta:
        abstract = True

class Poll(VoteObject):
    admins = models.ManyToManyField(User)
    viewers = models.ManyToManyField(User,related_name="view_only_users",blank=True)
    begin_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    restrict_to = models.ManyToManyField(Group,blank=True)
    allow_edits = models.BooleanField(default=False)
    display_mode = models.PositiveSmallIntegerField(default=0,choices=(
        (0,"Normal"),
    ))
    enabled = models.BooleanField(default=False)
    confirmation = models.TextField(blank=True,null=True)

    def _get_admins(self):
        return ", ".join([str(i) for i in self.admins.all()])
    _get_admins.short_description = "Admins"

    def get_absolute_url(self):
        return reverse("voting.views.vote",args=(self.id,))

    def is_open(self):
        now = timezone.now()
        if self.begin_date:
            if self.begin_date > now:
                return False
        if self.end_date:
            if self.end_date < now:
                return False
        return True

    def user_allowed(self,user=None,cache=False):
        if cache:
            self._cached_user_allowed = self.user_allowed(user)
        if (not user) and (not hasattr(self,"_cached_user_allowed")):
            raise TypeError("Must supply user without previous cached value!")
        return (getattr(self,"_cached_user_allowed",False) if not user else
                (not ((not self.allow_edits) and Response.objects.filter(
                    user=user, question=Question.objects.filter(poll=self)[0]).exists())))

class Choice(VoteObject):
    content_type = models.ForeignKey(ContentType,blank=True,null=True,default=None)
    object_id = models.PositiveIntegerField(blank=True,null=True,default=None)
    obj = GenericForeignKey()

class Question(VoteObject):
    poll = models.ForeignKey(Poll)
    kind = models.PositiveSmallIntegerField(default=0,choices=(
        (0, "Highest Wins"),
        (1, "IRV"),
        (2, "Fill-in"),
        (3, "Highest Points"),
    ))
    choices = models.ManyToManyField(Choice)

class Response(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice,blank=True,null=True)
    choice_extra = models.CharField(max_length=512,blank=True,null=True)

    def __str__(self):
        return "{user}'s response to {question}: {choice} ({choice_extra})".format(
            user=self.user.get_full_name(), question=self.question,
            choice=self.choice, choice_extra=self.choice_extra)

class HighestPointsOptions(models.Model):
    question = models.OneToOneField(Question, models.CASCADE)
    points = ArrayField(models.PositiveIntegerField())
    winners = models.PositiveSmallIntegerField()
