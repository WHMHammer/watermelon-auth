from datetime import datetime, timedelta, timezone
from hashlib import scrypt
from os import urandom
from random import randint
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, BINARY, TIMESTAMP, TINYINT, VARCHAR
from sqlalchemy.ext.hybrid import hybrid_property

from info.auth import *
from lib import *


def assert_id(id):
    if id is None:
        raise IDNullError
    if not isinstance(id, int):
        raise IDTypeError(id)
    if id < id_min_value or id > id_max_value:
        raise IDValueError(id)


def assert_email(email):
    if email in ("", None):
        raise EmailNullError
    if not isinstance(email, str):
        raise EmailTypeError(email)
    if len(email) > email_max_length:
        raise EmailTooLongError(email)


def assert_timestamp(timestamp):
    if timestamp is None:
        raise TimestampNullError
    if not isinstance(timestamp, datetime):
        raise TimestampTypeError(timestamp)
    if timestamp.tzinfo != timezone.utc:
        raise TimestampTimezoneError(timestamp.tzinfo)


def assert_salt(salt):
    if salt is None:
        raise SaltNullError
    if not isinstance(salt, bytes):
        raise SaltTypeError(salt)
    if len(salt) != salt_length:
        raise SaltLengthError(salt)


def assert_password(password):
    if password is None:
        raise PasswordNullError
    if not isinstance(password, str):
        raise PasswordTypeError(password)
    if len(password) < password_min_length:
        raise PasswordTooShortError


def assert_password_encrypted(password_encrypted):
    if password_encrypted is None:
        raise PasswordEncryptedNullError
    if not isinstance(password_encrypted, bytes):
        raise PasswordEncryptedTypeError(password_encrypted)
    if len(password_encrypted) != password_encrypted_length:
        raise PasswordEncryptedLengthError(password_encrypted)


def assert_ip(ip):
    if ip in ("", None):
        raise IPNullError
    if not isinstance(ip, str):
        raise IPTypeError(ip)
    try:
        ip0, ip1, ip2, ip3 = ip.split(".")
        ip0 = int(ip0)
        ip1 = int(ip1)
        ip2 = int(ip2)
        ip3 = int(ip3)
    except ValueError:
        raise IPFormatError(ip)
    return ip0, ip1, ip2, ip3


class User(Base):
    __tablename__ = "user"
    _id = Column("id", BIGINT, unique=True, nullable=False, primary_key=True)
    _email = Column("email", VARCHAR(64), unique=True, nullable=False)
    _register_time = Column("register_time", TIMESTAMP, nullable=False)
    _salt = Column("salt", BINARY(16), nullable=False)
    _password_encrypted = Column(
        "password_encrypted", BINARY(64), nullable=False)

    def __repr__(self):
        return f"User(\n\tid={repr(self.id)},\n\temail={repr(self.email)},\n\tregister_time={repr(self.register_time)}\n)"

    def jsonfy(self):
        return {
            "id": self.id,
            "email": self.email,
            "register_time": round(self.register_time.timestamp())
        }

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        assert_id(id)
        self._id = id

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        assert_email(email)
        self._email = email

    @hybrid_property
    def register_time(self):
        return self._register_time

    @register_time.setter
    def register_time(self, register_time):
        assert_timestamp(register_time)
        self._register_time = register_time

    @hybrid_property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self, salt):
        assert_salt(salt)
        self._salt = salt

    @hybrid_property
    def password_encrypted(self):
        return self._password_encrypted

    @password_encrypted.setter
    def password_encrypted(self, password_encrypted):
        assert_password_encrypted(password_encrypted)
        self._password_encrypted = password_encrypted


class Session(Base):
    __tablename__ = "session"
    _id = Column("id", BIGINT, unique=True, nullable=False, primary_key=True)
    _user_id = Column("user_id", BIGINT, ForeignKey(
        "user.id"), nullable=False, primary_key=True)
    _ip0 = Column("ip0", TINYINT, nullable=False)
    _ip1 = Column("ip1", TINYINT, nullable=False)
    _ip2 = Column("ip2", TINYINT, nullable=False)
    _ip3 = Column("ip3", TINYINT, nullable=False)
    _expire_time = Column("expire_time", TIMESTAMP, nullable=False)

    def __repr__(self):
        return f"Session(\n\tid={repr(self.id)},\n\tuser_id={repr(self.user_id)},\n\tip={repr(self.ip)},\n\texpire_time={repr(self.expire_time)}\n)"

    def jsonfy(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expire_time": int(self.expire_time.timestamp())
        }

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        assert_id(id)
        self._id = id

    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        assert_id(user_id)
        self._user_id = user_id

    @hybrid_property
    def ip(self):
        return f"{self._ip0}.{self._ip1}.{self._ip2}.{self._ip3}"

    @ip.setter
    def ip(self, ip):
        self._ip0, self._ip1, self._ip2, self._ip3 = assert_ip(ip)

    @hybrid_property
    def expire_time(self):
        return self._expire_time

    @expire_time.setter
    def expire_time(self, expire_time):
        assert_timestamp(expire_time)
        self._expire_time = expire_time


def encrypt_password(password, salt):
    assert_password(password)
    assert_salt(salt)
    return scrypt(password.encode("utf-8"), salt=salt, n=scrypt_n, r=scrypt_r, p=scrypt_p)


@db_wrapper(always_return=True)
def user_exists(**kwargs):
    """
    db_session
    user_id
    email
    """
    db_session = kwargs["db_session"]
    user_id = kwargs.get("user_id")
    email = kwargs.get("email")
    if user_id is not None:
        assert_id(user_id)
        return bool(db_session.query(User).filter_by(id=user_id).count())
    if email is not None:
        assert_email(email)
        return bool(db_session.query(User).filter_by(email=email).count())
    raise ValueError


@db_wrapper()
def get_user_by_id(**kwargs):
    """
    db_session
    user_id
    """
    db_session = kwargs["db_session"]
    user_id = kwargs.get("user_id")
    assert_id(user_id)
    try:
        user = db_session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        raise UserDoesNotExistError
    return user


@db_wrapper()
def user_id_to_user(**kwargs):
    """
    db_session
    user
    """
    db_session = kwargs["db_session"]
    user = kwargs.get("user")
    if isinstance(user, User):
        return user
    if isinstance(user, int):
        assert_id(user)
        return get_user_by_id(
            db_session=db_session,
            user_id=user
        )
    raise TypeError


def user_to_user_id(user):
    if isinstance(user, int):
        return user
    if isinstance(user, User):
        return user.id
    raise TypeError


@db_wrapper()
def create_session(**kwargs):
    """
    db_session
    user
    ip
    expire_time
    """
    db_session = kwargs["db_session"]
    user_id = user_to_user_id(kwargs.get("user"))
    ip = kwargs.get("ip")
    assert_ip(ip)
    expire_time = kwargs.get("expire_time", datetime.now(
        timezone.utc)+timedelta(days=1))
    assert_timestamp(expire_time)

    session = Session()
    session.user_id = user_id
    session.ip = ip
    session.expire_time = expire_time
    while True:
        session.id = randint(id_min_value, id_max_value)
        db_session.add(session)
        try:
            db_session.commit()
        except IntegrityError:
            continue
        else:
            return session


@db_wrapper()
def clear_sessions(**kwargs):
    """
    db_session
    user
    time_limit
    """
    db_session = kwargs["db_session"]
    user_id = user_to_user_id(kwargs.get("user"))
    time_limit = kwargs.get("time_limit", datetime.now(timezone.utc))
    assert_timestamp(time_limit)
    db_session.query(Session).filter(Session.user_id == user_id,
                                     Session.expire_time < time_limit.replace(tzinfo=None)).delete()
    db_session.commit()


@db_wrapper()
def get_user_by_session(**kwargs):
    """
    db_session
    session_id
    user_id
    ip
    """
    db_session = kwargs["db_session"]
    session_id = kwargs.get("session_id")
    assert_id(session_id)
    user_id = kwargs.get("user_id")
    user = get_user_by_id(
        db_session=db_session,
        user_id=user_id
    )
    ip = kwargs.get("ip")
    ip0, ip1, ip2, ip3 = assert_ip(ip)
    try:
        session = db_session.query(Session).filter_by(
            id=session_id,
            user_id=user_id,
            _ip0=ip0,
            _ip1=ip1,
            _ip2=ip2,
            _ip3=ip3
        ).one()
    except NoResultFound:
        raise WrongSessionError
    if session.expire_time < datetime.utcnow():
        raise SessionExpiredError
    clear_sessions(
        db_session=db_session,
        user=user
    )
    return user


@db_wrapper()
def register_user(**kwargs):
    """
    db_session
    email
    password
    """
    db_session = kwargs["db_session"]
    email = kwargs.get("email")
    assert_email(email)
    password = kwargs.get("password")
    assert_password(password)
    if not isinstance(password, str):
        raise TypeError
    if user_exists(
        db_session=db_session,
        email=email
    ):
        raise UserExistsError(email)
    user = User()
    user.email = email
    try:
        send_email(noreply, email, register_email_subject, register_email_body)
    except smtplib.SMTPRecipientsRefused:
        raise EmailInvalidError
    user.register_time = datetime.now(timezone.utc)
    user.salt = urandom(16)
    user.password_encrypted = encrypt_password(password, user.salt)
    while True:
        user.id = randint(id_min_value, id_max_value)
        db_session.add(user)
        try:
            db_session.commit()
        except IntegrityError:
            continue
        else:
            return user


@db_wrapper()
def update_user_email(**kwargs):
    """
    db_session
    user
    email
    """
    db_session = kwargs["db_session"]
    user = user_id_to_user(
        db_session=db_session,
        user=kwargs.get("user")
    )
    email = kwargs.get("email")
    assert_email(email)

    try:
        send_email(noreply, email, change_email_new_email_subject,
                   change_email_new_email_body % user.email)
    except smtplib.SMTPRecipientsRefused:
        raise EmailInvalidError

    try:
        send_email(noreply, user.email, change_email_old_email_subject,
                   change_email_old_email_body % email)
    except smtplib.SMTPRecipientsRefused:
        pass

    user.email = email
    db_session.commit()


@db_wrapper()
def update_user_password(**kwargs):
    """
    db_session
    user
    password
    """
    db_session = kwargs["db_session"]
    user = user_id_to_user(
        db_session=db_session,
        user=kwargs.get("user")
    )
    password = kwargs.get("password")
    assert_password(password)

    try:
        send_email(noreply, user.email, change_password_email_subject,
                   change_password_email_body)
    except smtplib.SMTPRecipientsRefused:
        pass

    user.salt = urandom(16)
    user.password_encrypted = encrypt_password(password, user.salt)
    db_session.commit()


@db_wrapper()
def delete_user(**kwargs):
    """
    db_session
    user
    """
    db_session = kwargs["db_session"]
    user = user_id_to_user(
        db_session=db_session,
        user=kwargs.get("user")
    )

    email = user.email
    db_session.delete(user)
    db_session.commit()
    send_email(noreply, email, delete_user_email_subject,
               delete_user_email_body)


@db_wrapper()
def log_in(**kwargs):
    """
    db_session
    email
    password
    ip
    """
    db_session = kwargs["db_session"]
    email = kwargs.get("email")
    assert_email(email)
    password = kwargs.get("password")
    assert_password(password)
    ip = kwargs.get("ip")
    assert_ip(ip)
    try:
        user = db_session.query(User).filter_by(email=email).one()
    except NoResultFound:
        raise UserDoesNotExistError(email)
    if encrypt_password(password, user.salt) != user.password_encrypted:
        raise WrongPasswordError
    clear_sessions(
        db_session=db_session,
        user=user,
    )
    return create_session(
        db_session=db_session,
        user=user,
        ip=ip
    )


@db_wrapper()
def log_out(**kwargs):
    """
    db_session
    user
    session_id
    """
    db_session = kwargs["db_session"]
    user_id = user_to_user_id(kwargs.get("user"))
    session_id = kwargs.get("session_id")
    assert_id(session_id)

    db_session.query(Session).filter(Session.user_id ==
                                     user_id, Session.id == session_id).delete()
    db_session.commit()
