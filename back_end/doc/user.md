# [back_end](./back_end.md)/user

## `assert_id(id)`

- `id`: `int`, the `id` column of the `user` and the `id` column of the `session` table

The range of `id` is defined in `id_min_value` and `id_max_value` in /info/user.py.

## `assert_email(email)`

- `email`: `str`, the `email` column of the `user` table

The maximum length of `email` is defined in `email_max_length` in /info/user.py.

## `assert_timestamp(timestamp)`

- `timestamp`: `datetime.datetime`, the `register_time` column of the `user` table and the `expire_time` column of the `session` table

All timestamps should be in the UTC timezone.

## `assert_salt(salt)`

- `salt`: `bytes`, the `salt` column of the `user` table

The length of `salt` is defined in `salt_length` in /info/user.py.

## `assert_password(password)`

- `password`: `str`, the raw password sent by user

## `assert_password_encrypted(password_encrypted)`

- `password_encrypted`: `bytes`, the `password_encrypted` column of the `user` table

The length of `password_encrypted` is defined in `password_encrypted_length` in /info/user.py.

## `assert_ip(ip)`

- `ip`: `str`, the `ip0`, `ip1`, `ip2`, `ip3` columns of the `session` table

`ip` = `ip0`.`ip1`.`ip2`.`ip3`.

## `encrypt_password(password, salt)`

- `password`: `str`, the raw password sent by user

- `salt`: `bytes`, a random byte array

Returns the encrypted (using scrypt) password in `bytes`. The parameters of scrypt are defined in `scrypt_n`, `scrypt_r`, and `scrypt_p` in /info/user.py

## `exists(email, db_session=DBSession())`

- `email`: `str`, the email address to be checked

- `db_session`: a db session returned by `DBSession()`

Returns `True` if the email address has been registered before, `False` otherwise.

## `create_session(user, ip, db_session=DBSession())`

- `user`: `User`, the user object to be created a session for

- `ip`: `str`, the ip address to be created a session with

- `db_session`: a db session returned by `DBSession()`

Creates and a session record in the database. Returns in `Session` if a `db_session` is given.

## `clear_sessions(user, timestamp=datetime.utcnow(), db_session=DBSession())`

- `user`: `User`, the user object to be cleared all sessions for

- `timestamp`: `datetime.datetime`, the time all expiration time to be checked against

- `db_session`: a db session returned by `DBSession()`

Deletes all sessions with expiration time earlier than the given timestamp for the given user.

## `register(email, password, ip="0.0.0.0", db_session=DBSession())`

- `email`: `str`, the email address to be registered with

- `password`: `str`, the raw password

- `ip`: `str`, used to create a log in session after a successful registration

- `db_session`: a db session returned by `DBSession()`

Creates a registration record in the database, send an email to the user, and creates a log in session record in the database on success. Returns in `(User, Session)` if a `db_session` is given.

## `log_in(email, password, ip, db_session=DBSession())`

- `email`: `str`, the email address to be logged in with

- `password`: `str`, the raw password

- `ip`: `str`, used to create a log in session after a successful registration

- `db_session`: a db session returned by `DBSession()`

Verifies user's identity, and creates a log in session record in the database on success. Returns in `(User, Session)` if a `db_session` is given.
