import os

from flask import Flask, render_template


def create_app():
    # create and configure the app
    app = Flask(__name__, static_folder = './dist',)

    from pyQstat import hosts, jobs, queues

    app.register_blueprint(hosts.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(queues.bp)

    @app.route("/")
    def homepage():
        return render_template("homepage.html", title="Home")

    return app
