#!/usr/bin/python
import logging
import os
import sys

PYTHON_MAJOR = sys.version_info[0]

# =======================
# make sure this is correct!
# =======================
install_dir = "/var/www/html/pyQstat"
activate_this = os.path.join(install_dir, "venv/bin/activate_this.py")
# =======================

if PYTHON_MAJOR == 2:
    execfile(activate_this, dict(__file__=activate_this))
else:
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, install_dir)

# =======================
# And this too!
# =======================
os.environ["PATH"] += os.pathsep + "/opt/gridengine/bin/lx-amd64"
os.environ["SGE_ROOT"] = "/opt/gridengine"
os.environ["SGE_QMASTER_PORT"] = "536"
os.environ["SGE_EXECD_PORT"] = "537"
# =======================

if True:
    from pyQstat import create_app

application = create_app()
