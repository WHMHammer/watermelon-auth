import smtplib

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from typing import *

from info import *

engine = create_engine(f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}")
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

def db_wrapper(always_return: bool=False):
    def decor(foo):
        def bar(*args, db_session=None, **kwargs):
            if not db_session:
                try:
                    db_session = DBSession()
                    r = foo(*args+(db_session,), **kwargs)
                    if always_return:
                        return r
                    else:
                        return
                finally:
                    db_session.close()
            return foo(*args+(db_session,), **kwargs)
        return bar
    return decor

def send_email(sender: Dict[str, Union[str, int]], receivers: Union[str, List[str], Tuple[str], Set[str], Dict[str, Any]], subject: str, body: str):
    with smtplib.SMTP_SSL(sender.get("smtp_server"), sender.get("port")) as conn:
        conn.login(sender.get("address"), sender.get("token"))
        if isinstance(receivers, str):
            receivers = (receivers,)
        for to in receivers:
            conn.sendmail(
                sender.get("address"),
                to,
                bytes("Sender: %s\nTo: %s\nSubject: %s\nContent-Type: text/html\n\n%s" % (
                    sender.get("address"),
                    to,
                    subject,
                    body
                ), "utf8")
            )
