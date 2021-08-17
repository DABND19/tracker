from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, String, BigInteger, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    full_name = Column(String(64))
    is_superuser = Column(Boolean, default=False, nullable=False)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(BigInteger, primary_key=True)
    title = Column(String(128), nullable=False)


class Reply(Base):
    __tablename__ = "replies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_time = Column(DateTime, nullable=False)
    reply_time = Column(DateTime, nullable=False)
    employee = Column(Integer, ForeignKey(Employee.id), nullable=False)
    chat = Column(BigInteger, ForeignKey(Chat.id), nullable=False)
