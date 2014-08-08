from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

from django.conf import settings
import django
django.setup()

import sys, re

from importlib import import_module

DEBUG = ("debug" in sys.argv) or settings.DEBUG

handlers = []

for i in settings.INSTALLED_APPS:
    try:
        module = import_module(i+".websockets")
        for url in module.urls:
            url.regex = re.compile("/" + i + url.reverse())
        handlers += module.urls
    except ImportError:
        pass

if DEBUG: print(handlers)

application = Application(handlers,debug=DEBUG)

def main():
    host, colon, port = sys.argv[1].rpartition(":")
    application.listen(int(port),host)
    IOLoop.current().start()
