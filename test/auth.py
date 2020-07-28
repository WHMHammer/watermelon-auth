from requests import get, post, put, delete
from time import time

base_url = "http://localhost:8080"
id_min_value = 0
id_max_value = 18446744073709551615
email_max_length = 64
password_min_length = 8
email = ""
password = ""
email1 = ""
password1 = ""


def print_error_response(r):
    print(r.status_code)
    print(r.text)
    raise Exception


def test_back_end():
    # registeration test begin
    # email missing
    r = post(base_url+"/auth/user", json={
        "password": password
    })
    if r.status_code != 400:
        print_error_response(r)

    # email empty
    r = post(base_url+"/auth/user", json={
        "email": "",
        "password": password
    })
    if r.status_code != 403 or r.json().get("err_msg") != "EmailNullError":
        print_error_response(r)

    # email too long
    r = post(base_url+"/auth/user", json={
        "email": "@"*(email_max_length+1),
        "password": password
    })
    if r.status_code != 403 or r.json().get("err_msg") != "EmailTooLongError":
        print_error_response(r)

    # email invalid
    r = post(base_url+"/auth/user", json={
        "email": "@",
        "password": password
    })
    if r.status_code != 403 or r.json().get("err_msg") != "EmailInvalidError":
        print_error_response(r)

    # password missing
    r = post(base_url+"/auth/user", json={
        "email": email
    })
    if r.status_code != 400:
        print_error_response(r)

    # password too short
    r = post(base_url+"/auth/user", json={
        "email": email,
        "password": ""
    })
    if r.status_code != 403 or r.json().get("err_msg") != "PasswordTooShortError":
        print_error_response(r)

    # valid registration
    r = post(base_url+"/auth/user", json={
        "email": email,
        "password": password
    })
    if r.status_code != 200:
        print_error_response(r)
    user_id = r.json().get("user_id")
    session_id = r.json().get("session_id")

    # duplicate registration
    r = post(base_url+"/auth/user", json={
        "email": email,
        "password": password
    })
    if r.status_code != 403 or r.json().get("err_msg") != "UserExistsError":
        print_error_response(r)
    # registration test ends

    # get user profile test begin
    # user_id missing
    r = get(base_url+f"/auth/user", params={
        "session_id": session_id
    })
    if r.status_code != 400:
        print_error_response(r)

    # user_id too small
    r = get(base_url+f"/auth/user", params={
        "user_id": id_min_value-1,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # user_id too large
    r = get(base_url+f"/auth/user", params={
        "user_id": id_max_value+1,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # user does not exist
    r = get(base_url+f"/auth/user", params={
        "user_id": id_max_value-user_id,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "UserDoesNotExistError":
        print_error_response(r)

    # session_id missing
    r = get(base_url+f"/auth/user", params={
        "user_id": user_id
    })
    if r.status_code != 400:
        print_error_response(r)

    # session_id too small
    r = get(base_url+f"/auth/user", params={
        "session_id": id_min_value-1,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # session_id too large
    r = get(base_url+f"/auth/user", params={
        "session_id": id_max_value+1,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # session does not exist
    r = get(base_url+f"/auth/user", params={
        "session_id": id_max_value-session_id,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "WrongSessionError":
        print_error_response(r)

    # valid session
    r = get(base_url+f"/auth/user", params={
        "user_id": user_id,
        "session_id": session_id
    })
    if r.status_code != 200:
        print_error_response(r)
    r_json = r.json()
    if r_json.get("id") != user_id or r_json.get("email") != email or r_json.get("register_time") > int(time()+1):
        print_error_response(r)
    # get user profile test end

    # update user profile begin
    # user_id missing
    r = put(base_url+f"/auth/user", json={
        "session_id": session_id
    })
    if r.status_code != 400:
        print_error_response(r)

    # user_id too small
    r = put(base_url+f"/auth/user", json={
        "user_id": id_min_value-1,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # user_id too large
    r = put(base_url+f"/auth/user", json={
        "user_id": id_max_value+1,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # user does not exist
    r = put(base_url+f"/auth/user", json={
        "user_id": id_max_value-user_id,
        "session_id": session_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "UserDoesNotExistError":
        print_error_response(r)

    # session_id missing
    r = put(base_url+f"/auth/user", json={
        "user_id": user_id
    })
    if r.status_code != 400:
        print_error_response(r)

    # session_id too small
    r = put(base_url+f"/auth/user", json={
        "session_id": id_min_value-1,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # session_id too large
    r = put(base_url+f"/auth/user", json={
        "session_id": id_max_value+1,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "IDValueError":
        print_error_response(r)

    # session does not exist
    r = put(base_url+f"/auth/user", json={
        "session_id": id_max_value-session_id,
        "user_id": user_id
    })
    if r.status_code != 403 or r.json().get("err_msg") != "WrongSessionError":
        print_error_response(r)

    # valid session and email
    r = put(base_url+f"/auth/user", json={
        "user_id": user_id,
        "session_id": session_id,
        "email": email1
    })
    if r.status_code != 200:
        print_error_response(r)
    r = post(base_url+"/auth/session", json={
        "email": email1,
        "password": password
    })
    if r.status_code != 200 or r.json().get("user_id") != user_id:
        print_error_response(r)

    # valid session and password
    r = put(base_url+f"/auth/user", json={
        "user_id": user_id,
        "session_id": session_id,
        "password": password1
    })
    if r.status_code != 200:
        print_error_response(r)
    r_json = r.json()
    r = post(base_url+"/auth/session", json={
        "email": email1,
        "password": password1
    })
    if r.status_code != 200 or r.json().get("user_id") != user_id:
        print_error_response(r)

    # valid session and email and password
    r = put(base_url+f"/auth/user", json={
        "user_id": user_id,
        "session_id": session_id,
        "email": email,
        "password": password
    })
    if r.status_code != 200:
        print_error_response(r)
    r_json = r.json()
    r = post(base_url+"/auth/session", json={
        "email": email,
        "password": password
    })
    if r.status_code != 200 or r.json().get("user_id") != user_id:
        print_error_response(r)
    # update user profile end

    # log in test begin

    # log in test end

    # log out test begin

    # log out test end

    # delete user test begin

    # delete user test end

    print("All tests passed.")


if __name__ == "__main__":
    test_back_end()
