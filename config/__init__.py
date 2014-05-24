

from . import models

class _Config:
    def __getattr__(self,key):
        return models.Config.get(key)
    __getitem__ = __getattr__

    def __setattr__(self,key,value):
        return models.Config.set(key,value)
    __setitem__ = __setattr__

    def get(self,key,fallback=None):
        return models.Config.get(key,fallback)

config = _Config()
