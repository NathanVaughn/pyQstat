import os
from datetime import datetime

from flask import Flask, render_template


def create_app():
    # create and configure the app
    app = Flask(__name__, static_folder = './dist',)

    from pyQstat import hosts, jobs, queues

    app.register_blueprint(hosts.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(queues.bp)

    @app.context_processor
    def inject_now():
        now = datetime.now().strftime("%a, %d %b %Y %X %z")
        return {'now': now}

    @app.route("/")
    def homepage():
        return render_template("homepage.html", title="Home")

    return app
