from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("queues", __name__)


@bp.route("/queues")
def all():
    queues = data.get_queues()
    ordering = [[0, "asc"]]

    return render_template(
        "queues/queues.html", queues=queues, ordering=ordering, title="Queues"
    )
