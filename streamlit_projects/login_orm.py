import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# main code for connection and database


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_pass = Column(String)
    user_email = Column(String)
    user_sector = Column(String)
    inputs = relationship('UserInput', backref="users")


class UserInput(Base):
    __tablename__ = "userinputs"

    id = Column(Integer, primary_key=True)
    house_area = Column(Integer)
    no_of_rooms = Column(Integer)
    age = Column(Integer)
    location = Column(String)
    id_user = Column(Integer, ForeignKey("users.id"))
    user = relationship('User')


if __name__ == "__main__":
    engine = create_engine('sqlite:///reg_db.sqlite3')
    Base.metadata.create_all(engine)
