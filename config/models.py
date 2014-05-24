from django.db import models

# Create your models here.

_cache = {}

class Config(models.Model):
    key = models.CharField(max_length=40,primary_key=True,unique=True)
    value = models.CharField(max_length=240,blank=True)
    missing = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        try:
            del _cache[self.key]
        except KeyError:
            pass
        super().save(*args,**kwargs)

    def __repr__(self):
        return "<{}: {}>".format(self.key,self.value)

    def __str__(self):
        return self.value

    @classmethod
    def get(self,key,fallback=None):
        try:
            res = _cache[key]
        except KeyError:
            try:
                obj = self.objects.get(key=key)
                if obj.missing:
                    return fallback
                res = obj.value
                _cache[key] = res
            except self.DoesNotExist as err:
                self.objects.create(key=key,value=fallback or "",missing=True)
                return fallback
        return res

    @classmethod
    def set(self,key,val):
        obj = self.objects.get_or_create(key=key)
        obj.value = val
        obj.save()

def clear_cache():
    _cache.clear()
