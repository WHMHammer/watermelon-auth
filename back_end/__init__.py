import flask
import sqlalchemy

from lib import DBSession

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
    db_session = flask.g.pop("db_session")
    if db_session:
        db_session.close()
    r.headers.set("Access-Control-Allow-Origin", "*")
    r.headers.set("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, DELETE")
    r.headers.set("Access-Control-Allow-Headers", "Content-Type")
    r.headers.set("Content-Type", "application/json")
    return r

from auth import bp as auth_bp
app.register_blueprint(auth_bp)

# from event import bp as event_bp
# app.register_blueprint(event_bp)
