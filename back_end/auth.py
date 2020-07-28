import flask

from datetime import datetime, timezone
from simplejson import dumps
from time import time
from urllib.parse import unquote

from lib.auth import *

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/user", methods=("GET",))
def get_user_profile():
    try:
        user_id = int(flask.g.form["user_id"])
        session_id = int(flask.g.form["session_id"])
    except (KeyError, TypeError):
        return "{}", 400

    try:
        user = get_user_by_session(
            db_session=flask.g.db_session,
            session_id=session_id,
            user_id=user_id,
            ip=get_visitor_ip(flask.request)
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    return user.jsonfy()


@bp.route("/user", methods=("POST",))
def view_register_user():
    try:
        email = flask.g.form["email"]
        password = flask.g.form["password"]
    except (KeyError, TypeError):
        return "{}", 400
    ip = get_visitor_ip(flask.request)

    try:
        user = register_user(
            db_session=flask.g.db_session,
            email=email,
            password=password,
            ip=ip
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    session = create_session(
        db_session=flask.g.db_session,
        user=user,
        ip=ip
    )

    return dumps({
        "user_id": session.user_id,
        "session_id": session.id
    })


@bp.route("/user", methods=("PUT",))
def view_update_user_profile():
    try:
        user_id = int(flask.g.form["user_id"])
        session_id = int(flask.g.form["session_id"])
    except (KeyError, TypeError):
        return "{}", 400

    db_session = flask.g.db_session

    try:
        user = get_user_by_session(
            db_session=db_session,
            session_id=session_id,
            user_id=user_id,
            ip=get_visitor_ip(flask.request)
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    if (email := flask.g.form.get("email")):
        try:
            update_user_email(
                db_session=db_session,
                user=user,
                email=email
            )
        except UserError as e:
            return dumps({"err_msg": e.__class__.__name__}), 403

    if (password := flask.g.form.get("password")):
        try:
            update_user_password(
                db_session=db_session,
                user=user,
                password=password
            )
        except UserError as e:
            return dumps({"err_msg": e.__class__.__name__}), 403

    return "{}"


@bp.route("/user", methods=("DELETE",))
def view_delete_user():
    try:
        user_id = int(flask.g.form["user_id"])
        session_id = int(flask.g.form["session_id"])
    except (KeyError, TypeError):
        return "{}", 400
    db_session = flask.g.db_session

    try:
        user = get_user_by_session(
            db_session=db_session,
            session_id=session_id,
            user_id=user_id,
            ip=get_visitor_ip(flask.request)
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    try:
        delete_user(
            db_session=db_session,
            user=user
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    return "{}"


@bp.route("/session", methods=("POST",))
def view_log_in():
    try:
        email = flask.g.form["email"]
        password = flask.g.form["password"]
    except (KeyError, TypeError):
        return "{}", 400

    try:
        session = log_in(
            db_session=flask.g.db_session,
            email=email,
            password=password,
            ip=get_visitor_ip(flask.request),
        )
    except UserError as e:
        return dumps({"err_msg": e.__class__.__name__}), 403

    return dumps({
        "user_id": session.user_id,
        "session_id": session.id
    })


@bp.route("/session", methods=("DELETE",))
def view_log_out():
    try:
        user_id = int(flask.g.form["user_id"])
        session_id = int(flask.g.form["session_id"])
    except (KeyError, TypeError):
        return "{}", 400

    log_out(
        db_session=flask.g.db_session,
        user=user_id,
        session_id=session_id
    )

    return "{}"

# @bp.route("/password", methods=("GET",))
# def request_password_reset():
#     try:
#         email = unquote(str(flask.g.form["email"]))
#     except (KeyError, TypeError):
#         return "{}", 400

#     if not legal_email(email):
#         return "{}", 400

#     cur = flask.g.db.cursor()

#     cur.execute("""
#         SELECT id, username
#         FROM users
#         WHERE email = %s AND status=%s
#         LIMIT 1;
#     """, (email, "verified"))

#     try:
#         user_id, username = cur.fetchone()
#     except TypeError:
#         return "{}"

#     challenge = rand_str(32)

#     cur.execute("""
#         UPDATE users
#         SET status = %s
#         WHERE id = %s;
#     """, (challenge, user_id))

#     cur.execute("""
#         DELETE FROM sessions
#         WHERE user_id = %s;
#     """, (user_id,))

#     flask.g.db.commit()

#     reset_password_url = f"{domain}/auth/reset_password"
#     send_email(
#         noreply,
#         email,
#         f"Reset your password at {project_name}",
#         f"""
#             <p>Hello, dear {username}:</p>
#             <p>Your verification code is:</p>
#             <p><code>{challenge}</code></p>
#             <p>Please click <a href="{reset_password_url}">here</a> or paste the following url to your web browser to reset your password:</p>
#             <p>{reset_password_url}</p>
#             <br/>
#             <p>Best regards,</p>
#             <p>{project_name}</p>
#         """
#     )

#     return "{}"

# @bp.route("/password", methods=("PUT",))
# def reset_password():
#     try:
#         username = str(flask.g.form["username"])
#         email = str(flask.g.form["email"]).lower()
#         response = str(flask.g.form["response"])
#         salt = str(flask.g.form["salt"])
#         password_hash = str(flask.g.form["password_hash"])
#     except (KeyError, TypeError):
#         return "{}", 400

#     if not(
#         legal_username(username) and
#         legal_email(email) and
#         len(response) == 32 and
#         legal_salt(salt) and
#         legal_hash(password_hash)
#     ):
#         return "{}", 400

#     cur = flask.g.db.cursor()

#     cur.execute("""
#         SELECT *
#         FROM users
#         WHERE username = %s AND email = %s AND status = %s
#         LIMIT 1;
#     """, (username, email, response))

#     if cur.fetchone() is None:
#         return "{}", 403

#     cur.execute("""
#         UPDATE users
#         SET status = %s, salt = %s, password_hash = %s
#         WHERE username=%s;
#     """, ("verified", salt, password_hash, username))

#     flask.g.db.commit()

#     send_email(
#         noreply,
#         email,
#         "You have successfully changed your password!",
#         f"""
#             <p>Hello, dear {username}:</p>
#             <p>You have successfully changed your password!</p>
#             <br/>
#             <p>Best regards,</p>
#             <p>{project_name}</p>
#         """
#     )

#     return dumps({
#         "user_token": generate_user_token(username)
#     })

# @bp.route("/user", methods=("GET",))
# def get_username():
#     try:
#         email = unquote(str(flask.g.form["email"]))
#     except (KeyError, TypeError):
#         return "{}", 400

#     if not(
#         legal_email(email)
#     ):
#         return "{}", 400

#     cur = flask.g.db.cursor()

#     cur.execute("""
#         SELECT username
#         FROM users
#         WHERE email = %s AND status = %s
#         LIMIT 1;
#     """, (email, "verified"))

#     try:
#         username = cur.fetchone()[0]
#     except TypeError:
#         pass
#     else:
#         send_email(
#             noreply,
#             email,
#             f"Your username at {project_name}",
#             f"""
#                 <p>Your username at {project_name} is:</p>
#                 <p>{username}</p>
#                 <br/>
#                 <p>Best regards,</p>
#                 <p>{project_name}</p>
#             """
#         )

#     return "{}"

# @bp.route("/user", methods=("PUT",))
# def update_user_info():
#     user = get_user_token(flask.g.form.get("user_token", None))

#     if user is None:
#         return "{}", 401

#     cur = flask.g.db.cursor()

#     if "username" in flask.g.form:
#         username = str(flask.g.form["username"])
#         if not legal_username(username):
#             return "{}", 400

#         cur.execute("""
#             UPDATE users
#             SET username = %s
#             WHERE id = %s;
#         """, (username, user["user_id"]))

#     if "email" in flask.g.form:
#         email = str(flask.g.form["email"])
#         if not legal_email(email):
#             return "{}", 400

#         cur.execute("""
#             UPDATE users
#             SET email = %s
#             WHERE id = %s;
#         """, (email, user["user_id"]))

#     if "avatar" in flask.g.form:
#         avatar = str(flask.g.form["avatar"])
#         if not legal_url(avatar):
#             return "{}", 400

#         cur.execute("""
#             UPDATE users
#             SET avatar = %s
#             WHERE id = %s;
#         """, (avatar, user["user_id"]))

#     if "password_hash" in flask.g.form:
#         try:
#             salt = str(flask.g.form["salt"])
#             password_hash = str(flask.g.form["password_hash"])
#         except (KeyError, TypeError):
#             return "{}", 400

#         if not(
#             legal_salt(salt) and
#             legal_hash(password_hash)
#         ):
#             return "{}", 400

#         cur.execute("""
#             UPDATE users
#             SET salt = %s, password_hash = %s
#             WHERE id = %s;
#         """, (salt, password_hash, user["user_id"]))

#     flask.g.db.commit()

#     return "{}"

# @bp.route("/user", methods=("DELETE",))
# def delete_user():
#     user = get_user_token(flask.g.form.get("user_token", None))

#     if user is None:
#         return "{}"

#     cur = flask.g.db.cursor()

#     cur.execute("""
#         DELETE FROM sessions
#         WHERE user_id = %s;
#     """, (user["user_id"],))

#     cur.execute("""
#         DELETE FROM users
#         WHERE user_id = %s;
#     """, (user["user_id"],))

#     flask.g.db.commit()

#     return "{}"
