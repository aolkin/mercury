
from subprocess import *

def run_process(*args,**kwargs):
    try:
        return (0, check_output(args,stderr=STDOUT,**kwargs).decode().strip())
    except CalledProcessError as err:
        return (err.returncode, err.output.decode().strip())

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
        return run_process(self._compile_command,sourcefn)

    def run(self,sourcefn):
        return run_process(self._run_command,self.get_compiled_name(sourcefn))

    def get_compiled_name(self,fn):
        return fn

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
        return fn.rpartition(".")[0]

LANGUAGES = [
    Python2(),
    Python3(),
    Java(),
]
