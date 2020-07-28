const email_input = document.getElementById("email_input");
const email_warning_label = document.getElementById("user_does_not_exist");
const email_warning_label_user_already_exist = document.getElementById("wrong_password");
const email_warning_label_invalid_email = document.getElementById("invalid_email");
const password_input = document.getElementById("password_input");
const login_button = document.getElementById("login_button");
email_input.addEventListener("focusout", function (event) {
    let email = event.target.value;
    if (assert_email(email)) {
        email_warning_label_invalid_email.hidden = true;
    }
    else {
        email_warning_label_invalid_email.hidden = false;
    }
});
login_button.onclick = function () {
    let email = email_input.value;
    let password = password_input.value;
    if (!assert_email(email)) {
        alert("error");
        return;
    }
    let r = new XMLHttpRequest();
    r.onreadystatechange = function () {
        if (this.readyState == 4) {
            rp = JSON.parse(this.responseText);
            if (this.status == 400) {
                alert(400);
            }
            else if (this.status == 200) {
                localStorage.setItem("user", JSON.stringify(rp["user"]));
                localStorage.setItem("session", JSON.stringify(rp["session"]));
            }
            else if (this.status == 403) {
                if (rp.err_msg == "UserDoesNotExistError"){
                    email_warning_label.hidden = false;
                }
                if (rp.err_msg == "WrongPasswordError"){
                    email_warning_label_user_already_exist.hidden = false;
                }
            }
            else if (this.status == 404) {
                alert(404);
            }
        }
    };
    r.open("POST", "http://localhost:8080/auth/session");
    r.setRequestHeader("Content-Type", "application/json");
    r.send(JSON.stringify({
        "email": email,
        "password": password
    }));
};