const email_max_length = 64;
const mailformat = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

function assert_email(email) {
    if (!email) {
        return false;
    }
    if (email > email_max_length) {
        return false;
    }
    else{
        return mailformat.test(email);
    }
}
