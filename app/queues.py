from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from app import data

bp = Blueprint("queues", __name__)


@bp.route("/queues")
def all_queues():
    queues = data.get_queues()

    return render_template("queues/queues.html", queues=queues, title="Queues")
