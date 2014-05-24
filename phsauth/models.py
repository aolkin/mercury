from django.db import models

from django.conf import settings

from django.contrib.auth.models import User, Group

# Create your models here.

class LDAPGroup(Group):
    dn = models.CharField(max_length=160)
    kind = models.CharField(max_length=80,choices=(
        ("hr","Homeroom"),
        ("school","School"),
        ("type","Type"),
        (None,"Unknown")
    ),null=True,blank=True)

    def guess_type(self,nice=False,use_db=False):
        name = self.name
        if not name:
            return None
        elementary_hr = name.partition(" - ")
        if ( (name.replace(".","").isnumeric()) or
             (name[0].isalpha() and name[0].isupper() and name[1:].isnumeric()) or
             (elementary_hr[1] and elementary_hr[0].replace(" ","").isalpha() and elementary_hr[2].isnumeric()) ):
            if nice:
                return "HR"
            else:
                return "hr"
        else:
            for k,v in settings.LDAP_GROUP_MAPPINGS.items():
                if self.name in v:
                    if nice:
                        return k.title()
                    else:
                        return k
        return None

    def save(self,*args,**kwargs):
        self.kind = self.guess_type()
        super().save(*args,**kwargs)

    def __str__(self):
        return "{}: {}".format(self.guess_type(True) or "Unknown",self.name)

    class Meta:
        verbose_name = "LDAP Security Group"

class LDAPUser(User):
    dn = models.CharField(max_length=160,null=True)
    kind = models.CharField(max_length=80,null=True) # description
    home_dir = models.CharField(max_length=160,null=True)

    class Meta:
        verbose_name = "LDAP User"

    def update_from_LDAP(self,attrs):
        self.username = attrs["sAMAccountName"].lower()
        self.password = "ldap user"
        name = attrs["displayName"].partition(" ")
        self.first_name = name[0]
        self.last_name = name[2]

        self.dn = attrs["distinguishedName"]
        self.kind = attrs["description"]
        self.home_dir = attrs.get("homeDirectory","")

        self.save()
        groups = []
        for i in attrs.get("memberOf",[]):
            name = i.partition(",")[0].partition("=")[2]
            groups.append(LDAPGroup.objects.get_or_create(name=name,defaults={"dn":i})[0])
        self.groups = groups
        
        self.save()
        if getattr(self,self.kind.lower(),None):
            getattr(self,self.kind.lower()).update_from_LDAP(attrs)

class Student(LDAPUser):
    graduation_year = models.PositiveSmallIntegerField(null=True)
    sid = models.CharField(max_length=8,null=True)
    school = models.ForeignKey(LDAPGroup,null=True,blank=True,related_name="student_school")
    hr = models.ForeignKey(LDAPGroup,null=True,blank=True,related_name="student_hr")

    def update_from_LDAP(self,attrs):
        self.graduation_year = attrs["ppsyearofgraduation"]
        self.sid = attrs["ppsstudentnumber"]
        for i in self.groups.all():
            if i.ldapgroup:
                type_ = i.ldapgroup.guess_type()
                if type_ == "school":
                    self.school = i.ldapgroup
                elif type_ == "hr":
                    self.hr = i.ldapgroup
        self.save()
        self.groups.add(Group.objects.get_or_create(name=attrs["ppsyearofgraduation"])[0])

    class Meta:
        verbose_name = "Student"

class Teacher(LDAPUser):


    class Meta:
        verbose_name = "Teacher"

faculty = Teacher
