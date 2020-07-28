const email_input = document.getElementById("email_input");
const confirm_password_input = document.getElementById("confirm_password_input");
const email_warning_label_invalid_email_address = document.getElementById("email_warning_label");
const email_warning_label_user_already_exist = document.getElementById("repeat_email_warning_label");
const email_warning_label_invalid_email = document.getElementById("invalid_email_warning_label");
const email_warning_label_inconsist_password = document.getElementById("not_match_warning_label");
const password_input = document.getElementById("password_input");
const register_button = document.getElementById("register_button");
email_input.addEventListener("focusout", function (event) {
    let email = event.target.value;
    if (assert_email(email)) {
        email_warning_label_invalid_email_address.hidden = true;
    }
    else {
        email_warning_label_invalid_email_address.hidden = false;
    }
    email_warning_label_user_already_exist = true;
});
confirm_password_input.addEventListener("focusout", function (event) {
    let pw = password_input.value;
    let cpw = confirm_password_input.value;
    if (pw == cpw){
        email_warning_label_inconsist_password.hidden = true;
    }
    else{
        email_warning_label_inconsist_password.hidden = false;
    }
});
register_button.onclick = function () {
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
                alert("register success!");
                localStorage.setItem("user", JSON.stringify(rp["user"]));
                localStorage.setItem("session", JSON.stringify(rp["session"]));
                window.location.replace("/");
            }
            else if (this.status == 403) {
                if (rp.err_msg == "UserExistsError"){
                    email_warning_label_user_already_exist.hidden = false;
                }
                if (rp.err_msg == "EmailInvalidError"){
                    email_warning_label_invalid_email.hidden = false;
                }
            }
            else if (this.status == 404) {
                alert(404);
            }
        }
    };
    r.open("POST", "http://localhost:8080/auth/user");
    r.setRequestHeader("Content-Type", "application/json");
    r.send(JSON.stringify({
        "email": email,
        "password": password
    }));
};
