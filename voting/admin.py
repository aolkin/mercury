from django.contrib import admin

from django.db import models
from django.forms.widgets import TextInput

# Register your models here.

from .models import *

class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('name', 'desc', 'image', 'kind', 'choices')
    formfield_overrides = {
        models.TextField: { 'widget': TextInput }
    }
    min_num = 1
    extra = 0

class PollAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]
    save_on_top = True
    list_display = ("name","_get_admins")
    list_filter = ("begin_date","end_date")
    filter_horizontal = ("restrict_to","admins","viewers")
    fieldsets = (
        (None, {
            'fields': ("name","desc","image","admins","display_mode",'enabled')
        }),
        ('Limit by Date/Time', {
            'classes': ('collapse',),
            'fields': ('begin_date', 'end_date')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('confirmation','allow_edits','restrict_to','viewers')
        }),
    )

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    max_num = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ResponseInline,
    ]
    readonly_fields = ("poll",)
    exclude = ("kind","choices")
    list_display = ("poll","name","_imghtml")
    list_display_links = ("name",)

class ChoiceAdmin(admin.ModelAdmin):
    def get_model_perms(self,request):
        perms = super().get_model_perms(request)
        perms["add"] = False
        return perms

admin.site.register(Poll,PollAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)
