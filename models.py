from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.types import Boolean
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from kmail import send_mail

engine = create_engine('sqlite:///email.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class EmailBase(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    sent = Column(Boolean(create_constraint=False))

    def save(self, *args, **kwargs):
        session.add(self)
        session.commit()


def get_object(klass, **query):
    instance = session.query(klass).filter_by(**query).first()
    if not instance:
        return False
    return instance


def get_or_create(klass, **kwargs):
    o = get_object(klass, **kwargs), False
    if o[0]:
        return o
    else:
        sent = send_mail(kwargs['email'])
        instance = klass(**kwargs)
        instance.save()
        return instance, True


def init_db():
    Base.metadata.create_all(engine)
