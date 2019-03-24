#!/usr/bin/python
import logging
import os
import sys

PYTHON_MAJOR = sys.version_info[0]

install_dir = "/var/www/html/pyQstat"
activate_this = os.path.join(install_dir, "/venv/bin/activate_this.py")

if PYTHON_MAJOR == 2:
    execfile(activate_this, dict(__file__=activate_this))
else:
    exec(open(activate_this).read())

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, install_dir)

if True:
    from pyQstat import create_app

application = create_app()
