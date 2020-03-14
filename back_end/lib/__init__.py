import smtplib

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from info import *

engine = create_engine(f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}")
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

def send_email(sender, to, subject, body):
    with smtplib.SMTP_SSL(sender.get("smtp_server"), sender.get("port")) as conn:
        conn.login(sender.get("address"), sender.get("token"))
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
