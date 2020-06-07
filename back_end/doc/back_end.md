# back_end

## `db_wrapper(always_return=False)`

- `always_return`: `bool`, decides whether a result is returned even if a db_session is not given.

Returns a decorator that creates a new `DBSession` to be used in the decorated function if `db_session` is not given. e.g.

```
@db_wrapper()
def foo(a, b, db_session):
    # function body
```

When `foo(a, b)` is called, a `DBSession` is automatically instantiated and used as `db_session` to connect to the database. However, `None` will be returned regardless of what is returned in the original function. Use `@db_wrapper(always_return=True)` to return the original return value.

## `send_email(sender, receivers, subject, body)`

- `sender`: `Dict[str, Union[str, int]]`, stores the sender information. Check `noreply` in `info/__init.py` as an example.

- `receivers`: `Union[str, List[str], Tuple[str], Set[str], Dict[str, Any]]`, the email addresses of all receivers of the email.

- `subject`: `str`, the subject of the email.

- `body`: `str`, the body of the email.

Sends an email from the sender to all receivers.
