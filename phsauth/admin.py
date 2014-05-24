from django.contrib import admin

# Register your models here.

from .ldap import bulk_process_users
from .models import *

class GroupAdmin(admin.ModelAdmin):
    list_display = ("name","kind","dn")
    list_filter = ("kind",)
    readonly_fields = ("name","dn","kind")
    filter_horizontal = ("permissions",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("username","first_name","last_name","is_staff")
    search_fields = ("username","first_name","last_name")
    list_filter = ("kind","is_staff")
    filter_horizontal = ("groups","user_permissions")

    def get_search_results(self,request,queryset,search_term):
        if search_term.startswith("="):
            search_term = search_term[1:].strip()
            bulk_process_users("(samaccountname={}*)".format(search_term))
        elif search_term.startswith("++"):
            search_term = search_term[2:].strip()
            bulk_process_users("(sn=*{}*)".format(search_term))
        elif search_term.startswith("+"):
            search_term = search_term[1:].strip()
            bulk_process_users("(givenName=*{}*)".format(search_term))
        return super().get_search_results(request, queryset, search_term)

class HRFilter(admin.SimpleListFilter):
    title = "Homeroom"
    parameter_name = "hr"

    def lookups(self,request,model_admin):
        return LDAPGroup.objects.filter(kind="hr").values_list("id","name")

    def queryset(self,request,queryset):
        if self.value():
            return queryset.filter(hr=LDAPGroup.objects.get(id=self.value()))

class SchoolFilter(admin.SimpleListFilter):
    title = "School"
    parameter_name = "school"

    def lookups(self,request,model_admin):
        return LDAPGroup.objects.filter(kind="school").values_list("id","name")

    def queryset(self,request,queryset):
        if self.value():
            return queryset.filter(school=LDAPGroup.objects.get(id=self.value()))

class StudentAdmin(UserAdmin):
    list_display = ("username","first_name","last_name","school","is_staff")
    list_filter = ("kind","is_staff",SchoolFilter,HRFilter)

admin.site.register(LDAPGroup,GroupAdmin)
admin.site.register(LDAPUser,UserAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,UserAdmin)
