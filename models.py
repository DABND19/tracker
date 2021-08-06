from datetime import datetime, timedelta, time
from typing import Tuple
from sqlalchemy import Column, create_engine, ForeignKey, MetaData, delete
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import extract, select
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String, BigInteger, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import types


Base = declarative_base()
metadata = Base.metadata


class Employee(Base):
    __tablename__ = "Employee"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)


class Chat(Base):
    __tablename__ = "Chat"
    id = Column(BigInteger, primary_key=True)
    title = Column(String)

class Reply(Base):
    __tablename__ = "Reply"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    delta = Column(Integer)
    employee = Column(Integer, ForeignKey('Employee.id'))
    chat = Column(BigInteger, ForeignKey('Chat.id'))

