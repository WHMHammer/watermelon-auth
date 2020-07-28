from info import *

id_min_value = 0
id_max_value = 18446744073709551615


class UserError(Exception):
    pass


class IDError(UserError):
    pass


class IDNullError(IDError):
    pass


class IDTypeError(TypeError, IDError):
    pass


class IDValueError(ValueError, IDError):
    pass


class IDCollisionError(IDError):
    pass


email_max_length = 64


class EmailError(UserError):
    pass


class EmailNullError(EmailError):
    pass


class EmailTypeError(TypeError, EmailError):
    pass


class EmailTooLongError(ValueError, EmailError):
    pass


class EmailInvalidError(EmailError):
    pass


class TimestampError(UserError):
    pass


class TimestampNullError(TimestampError):
    pass


class TimestampTypeError(TypeError, TimestampError):
    pass


class TimestampTimezoneError(ValueError, TimestampError):
    pass


salt_length = 16


class SaltError(UserError):
    pass


class SaltNullError(SaltError):
    pass


class SaltTypeError(TypeError, SaltError):
    pass


class SaltLengthError(ValueError, SaltError):
    pass


password_min_length = 8


class PasswordError(UserError):
    pass


class PasswordNullError(PasswordError):
    pass


class PasswordTypeError(TypeError, PasswordError):
    pass


class PasswordTooShortError(ValueError, PasswordError):
    pass


password_encrypted_length = 64


class PasswordEncryptedError(UserError):
    pass


class PasswordEncryptedNullError(PasswordEncryptedError):
    pass


class PasswordEncryptedTypeError(TypeError, PasswordEncryptedError):
    pass


class PasswordEncryptedLengthError(ValueError, PasswordEncryptedError):
    pass


class IPError(UserError):
    pass


class IPNullError(IPError):
    pass


class IPTypeError(TypeError, IPError):
    pass


class IPFormatError(ValueError, IPError):
    pass


class UserQueryError(UserError):
    pass


class UserExistsError(UserQueryError):
    pass


class UserDoesNotExistError(UserQueryError):
    pass


class WrongPasswordError(UserError):
    pass


class SessionError(UserError):
    pass


class SessionExpiredError(SessionError):
    pass


class WrongSessionError(ValueError, SessionError):
    pass


scrypt_n = 2
scrypt_r = 8
scrypt_p = 1

register_email_subject = f"You have successfully registered at {project_name}"
register_email_body = f"""
    <p>Dear user:</p>
    <p>You have successfully registered at {project_name}. Thank you for your registration.</p>
    <p>Best regards,</p>
    <p>The {project_name} Team</p>
"""

change_email_new_email_subject = f"You have successfully changed your email address at {project_name}"
change_email_new_email_body = f"""
    <p>Dear user:</p>
    <p>You have successfully changed your email address from %s.
    <p>Best regards,</p>
    <p>The {project_name} Team</p>
"""
change_email_old_email_subject = f"You have successfully changed your email address at {project_name}"
change_email_old_email_body = f"""
    <p>Dear user:</p>
    <p>You have successfully changed your email address to %s.
    <p>Best regards,</p>
    <p>The {project_name} Team</p>
"""

change_password_email_subject = f"You have successfully changed your password at {project_name}"
change_password_email_body = f"""
    <p>Dear user:</p>
    <p>You have successfully changed your password.
    <p>Best regards,</p>
    <p>The {project_name} Team</p>
"""

delete_user_email_subject = f"You have successfully delete your account at {project_name}"
delete_user_email_body = f"""
    <p>Dear user:</p>
    <p>You have successfully deleted your account at {project_name}. We wish to see you again in the future.</p>
    <p>Best regards,</p>
    <p>The {project_name} Team</p>
"""
