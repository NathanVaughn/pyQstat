from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort

from pyQstat import data

bp = Blueprint("jobs", __name__)


@bp.route("/jobs")
def all_jobs():
    user_esc = request.args.get("user", default="*", type=str)
    queue_esc = request.args.get("queue", default="*", type=str)

    jobs = data.get_jobs(user_esc, queue_esc)
    ordering = [[0, "desc"]]

    return render_template("jobs/jobs.html", jobs=jobs, ordering=ordering, title="Jobs")

@bp.route("/jobs/<int:id>")
def single_job(id):
    job, messages = data.get_job(id)

    if job:
        return render_template("jobs/job.html", job=job, messages=messages, title="Job " + str(id))
    else:
        return render_template("error.html", title="Error", message="Job {} not found.".format(id))
