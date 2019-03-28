from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("hosts", __name__)


@bp.route("/hosts")
def all():
    hosts = data.get_hosts()

    return render_template("hosts/hosts.html", hosts=hosts, title="Hosts")
