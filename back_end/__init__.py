import flask
import sqlalchemy

from lib import DBSession

from auth import bp as auth_bp
#from event import bp as event_bp

app = flask.Flask(__name__)
app.DBSession = DBSession


@app.before_request
def before_all():
    if flask.request.method == "OPTIONS":
        return "{}"
    elif flask.request.method != "GET":
        flask.g.form = flask.request.get_json()
    else:
        flask.g.form = flask.request.args
    flask.g.db_session = flask.current_app.DBSession()


@app.after_request
def after_all(r):
    try:
        flask.g.pop("db_session").close()
    except KeyError:
        pass
    r.headers.set("Access-Control-Allow-Origin", "*")
    r.headers.set("Access-Control-Allow-Methods",
                  "OPTIONS, GET, POST, PUT, DELETE")
    r.headers.set("Access-Control-Allow-Headers", "Content-Type")
    r.headers.set("Content-Type", "application/json")
    return r


app.register_blueprint(auth_bp)
# app.register_blueprint(event_bp)
