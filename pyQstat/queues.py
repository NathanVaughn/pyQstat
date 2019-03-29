from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("queues", __name__)


@bp.route("/queues")
def list_queues():
    queues = data.get_queues()

    return render_template("queues/queues.html", queues=queues, title="Queues")
