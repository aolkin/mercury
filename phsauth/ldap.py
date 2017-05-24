from django.conf import settings

from ldap3 import *
import socket

from . import models
from django.contrib.auth.models import User

server = Server(settings.LDAP_SERVER,port=389)

class MasterBind:
    def __enter__(self):
        self.conn = Connection(server,auto_bind=True,authentication=AUTH_SIMPLE,
                               user=settings.LDAP_MASTER_USERNAME,
                               password=settings.LDAP_MASTER_PASSWORD)
        return self.conn

    def __exit__(self,type_,value,tb):
        self.conn.unbind()

def do_query(query,attrs=ALL_ATTRIBUTES):
    with MasterBind() as connection:
        if connection.search(settings.LDAP_SEARCH_BASE,query,attributes=attrs):
            try:
                res = []
                for k in  connection.response:
                    if k["type"] == "searchResEntry":
                        res.append({i: (j[0] if len(j) == 1 else j) for i,j in k["attributes"].items()})
                return res
            except KeyError as err:
                print(query,connection.response)
                return None
        else:
            return False

def search(s,attrs=ALL_ATTRIBUTES):
    return do_query("(name=*{}*)".format(s),attrs)

def getAttrs(username,attrs=ALL_ATTRIBUTES):
    res = do_query("(samaccountname={})".format(username))
    return res[0] if len(res) > 0 else None

def getDN(username):
    try:
        return getAttrs(username,["distinguishedName"])["distinguishedName"]
    except TypeError:
        return None

def authenticate(username,password):
    try:
        dn = getDN(username)
        if dn:
            auth_conn = Connection(server,auto_bind=True,authentication=AUTH_SIMPLE,
                                   user=dn,password=password)
            auth_conn.unbind()
            return (True,username)
        else:
            reason = "username"
    except LDAPException as err:
        reason = "password"
    return (False,reason)

def bulk_process_users(query):
    backend = LDAPBackend()
    for i in do_query(query):
        user = backend.get(i["sAMAccountName"],True)
        try:
            user.update_from_LDAP(i)
        except KeyError as err:
            print(i["name"],err)
            user.delete()

class LDAPBackend:
    def authenticate(self,username,password):
        res = authenticate(username,password)
        if res[0]:
            user = self.get(username,True)
            if user is None:
                return None
            attrs = getAttrs(username)
            user.update_from_LDAP(attrs)
            return user.user_ptr
        else:
            return None

    def get(self,username,ldapuser=False):
        try:
            user = models.LDAPUser.objects.get(username=username)
        except models.LDAPUser.DoesNotExist:
            attrs = getAttrs(username)
            if not attrs:
                return None
            if getattr(models,attrs.get("description", ''),None):
                getattr(models,attrs["description"])(username=username).save()
            else:
                return None
            user = models.LDAPUser.objects.get(username=username)
        if ldapuser:
            return user
        else:
            return user.user_ptr

    def get_user(self,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        return user # self.get(user.username)
