
from subprocess import *

from django.conf import settings

import os
from os.path import dirname, basename

def depriviledge():
    try:
        os.setgid(settings.UNPRIVILEDGED_UID)
        os.setuid(settings.UNPRIVILEDGED_UID)
    except Exception as err:
        print(repr(err))

def run_process(*args,**kwargs):
    try:
        return (0, check_output(args, stderr=STDOUT, universal_newlines=True,
                                preexec_fn=depriviledge, **kwargs).strip())
    except CalledProcessError as err:
        return (err.returncode, err.output.strip())

def get_output(*args,**kwargs):
    return run_process(*args,**kwargs)[1]

class Language:
    _run_command = "true"
    _compile_command = "true"

    def get_version(self):
        if hasattr(self,"_version"):
            return self._version
        else:
            self._set_version()
            return self._version

    def get_name(self):
        return self.get_version()

    def _set_version(self):
        self._version = "Dummy Language, v1.0"

    def compile(self,sourcefn):
        return run_process(self._compile_command, basename(sourcefn), cwd=dirname(sourcefn))

    def run(self,sourcefn,input=None,timeout=None):
        return run_process(self._run_command, self.get_compiled_name(sourcefn),
                           cwd=dirname(sourcefn), input=input, timeout=timeout)

    def get_compiled_name(self,fn):
        return basename(fn)

class Python2(Language):
    _run_command = "python2"

    def _set_version(self):
        self._version = get_output(self._run_command,"-V")

    def get_name(self):
        return self.get_version().split(".")[0]

class Python3(Python2):
    _run_command = "python3"

class Java(Language):
    _run_command = "java"
    _compile_command = "javac"

    def get_name(self):
        return "Java " + self.get_version().split('"')[1][2]

    def _set_version(self):
        self._version = get_output(self._run_command,"-version").split("\n")[0]

    def get_compiled_name(self,fn):
        return super().get_compiled_name(fn).rpartition(".")[0]

LANGUAGES = [
    Python2(),
    Python3(),
    Java(),
]
