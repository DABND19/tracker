from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, String, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Employee(Base):
    __tablename__ = "Employee"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)


class Chat(Base):
    __tablename__ = "Chat"
    id = Column(BigInteger, primary_key=True)
    title = Column(String)


class Reply(Base):
    __tablename__ = "Reply"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    delta = Column(Float)
    employee = Column(Integer, ForeignKey(Employee.id))
    chat = Column(BigInteger, ForeignKey(Chat.id))
