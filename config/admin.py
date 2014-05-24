from django.contrib import admin

# Register your models here.

from .models import *

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'missing')
    list_editable = ('value',)
    list_display_links = None
    list_filter = ('missing',)
    search_fields = ('key',)
    exclude = ('missing','date_modified')
    ordering = ('-missing','-date_modified')

    actions = ('clear_cache',)

    def save_model(self,request,obj,form,change):
        obj.missing = False
        obj.save()

    def clear_cache(self,request,queryset):
        clear_cache()
        self.message_user(request,"Cache cleared.")

admin.site.register(Config,ConfigAdmin)
