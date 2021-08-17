from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy.sql.sqltypes import DateTime, String, BigInteger, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

Base = declarative_base(metadata=meta)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(64))
    full_name = Column(String(64))
    is_superuser = Column(Boolean, default=False, nullable=False)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    title = Column(String(128), nullable=False)


class Reply(Base):
    __tablename__ = "replies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_time = Column(DateTime, nullable=False)
    reply_time = Column(DateTime, nullable=False)
    employee = Column(Integer, ForeignKey(Employee.id), nullable=False)
    chat = Column(BigInteger, ForeignKey(Chat.id), nullable=False)
