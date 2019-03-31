from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("hosts", __name__)


@bp.route("/hosts")
def list_hosts():
    hosts = data.get_hosts()

    #if hosts:
    return render_template("hosts/hosts.html", hosts=hosts, title="Hosts")
    #else:
    #    return render_template("error.html", title="Error", message="No hosts found.")
