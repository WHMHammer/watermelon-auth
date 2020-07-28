import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/register")
def register():
    return flask.render_template("auth/register.html")

@app.route("/login")
def login():
    return flask.render_template("auth/login.html")

@app.route("/user_info")
def user_info():
    return flask.render_template("auth/user_info.html")

@app.route("/alpha")
def alpha():
    return flask.render_template("alpha/index.html")

@app.route("/test")
def test():
    return flask.render_template("test/test_file.html")