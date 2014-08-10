#!/usr/bin/python3

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercury.settings")

from tornado_support.wsserver import main

if __name__ == "__main__":
    main()
