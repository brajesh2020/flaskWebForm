from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Date, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships, backref

engine = create_engine('mysql+mysqlconnector://root:@localhost/test', echo=True)
Base = declarative_base()


class User(Base):
    """"""
    __tablename__ = "usersinfo"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(25))
    email = Column(VARCHAR(25))
    password = Column(VARCHAR(120))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


Base.metadata.create_all(engine)
