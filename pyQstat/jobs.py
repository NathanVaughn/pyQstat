from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("jobs", __name__)


@bp.route("/jobs")
def all():
    jobs = data.get_jobs()
    #ordering = [[1, "desc"], [4, "asc"]]
    ordering = [[0, "desc"]]

    return render_template("jobs/jobs.html", jobs=jobs, ordering=ordering, title="Jobs")
