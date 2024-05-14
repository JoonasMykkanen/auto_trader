# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    models.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:56:01 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 09:50:51 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime as datetime_stamp
from datetime import date as date_stamp
from dataclasses import asdict
from json import dumps

from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from sqlalchemy import UniqueConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import Date

from .config import config
from .config import logger


class Base(MappedAsDataclass, DeclarativeBase):
    def to_dict(self) -> dict:
        dict_repr = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, date_stamp):
                value = value.isoformat()
            dict_repr[column.name] = value
        return dict_repr



############################################################################
#                                                                          #
#                              TICKER DATA                                 #
#                                                                          #
############################################################################
class Ticker(Base):
    """ Entrty from 'tickers' table in db \n\n id: serial id \n\n name: AAPL or NVDA \n\n index: SP500 or DOW """
    def __repr__(self) -> str:
        return f'id: {self.id!r}, name: {self.name!r}, index: {self.index!r}'
    
    __tablename__ = 'tickers'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    name: Mapped[str] = mapped_column(String(10), unique=True)
    index: Mapped[str] = mapped_column(String(50), nullable=False)
    company: Mapped[str] = mapped_column(String(50), nullable=False)

    
        

class DailyCandle(Base):
    def __repr__(self):
        return f'{self.date} - o: {self.open} h: {self.high} l: {self.low} c: {self.close}'
    
    __tablename__ = 'daily_candles'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)

    date: Mapped[date_stamp] = mapped_column(Date)
    open: Mapped[Float] =  mapped_column(Float, nullable=False)
    high: Mapped[Float] = mapped_column(Float, nullable=False)
    low: Mapped[Float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ticker_id: Mapped[int] = mapped_column(Integer, ForeignKey('tickers.id'))

    __table_args__  = (UniqueConstraint('date', 'ticker_id', name='date_daily_uc'),)



class WeeklyCandle(Base):
    """ Entry from 'weekly_candles table in db """
    __tablename__ = 'weekly_candles'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)

    date: Mapped[date_stamp] = mapped_column(Date)
    open: Mapped[Float] =  mapped_column(Float, nullable=False)
    high: Mapped[Float] = mapped_column(Float, nullable=False)
    low: Mapped[Float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ticker_id: Mapped[int] = mapped_column(Integer, ForeignKey('tickers.id'))

    __table_args__  = (UniqueConstraint('date', 'ticker_id', name='date_weekly_uc'),)





############################################################################
#                                                                          #
#                         USERS / WALLETS / MISC                           #
#                                                                          #
############################################################################
class User(Base):
    def __repr__(self) -> str:
        return f'name:  {self.firstname} {self.surname} \nbirthdaty:    {self.birthday} \nemail:    {self.email}\npwd_hash: {self.hash}'
    
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)

    # Personal info
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    surname: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[date_stamp] = mapped_column(Date)
    # phone: Mapped[str] = mapped_column(String(15), unique=True)

    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash: Mapped[str] = mapped_column(String(60))
    # TYPE (admin, user, superuser, etc...)
    # Register date

    # Reset every month
    voted: Mapped[bool] = mapped_column(Boolean)






############################################################################
#                                                                          #
#                    POSTS / LIKES / COMMENTS / REPLIES                    #
#                                                                          #
############################################################################
class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    title: Mapped[str] = mapped_column(String(50), unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime_stamp] = mapped_column(DateTime)
    author: Mapped[str] = mapped_column(String(50))

    # NOTE: Below will not be mapped to database
    vote_count = None


class Vote(Base):
    __tablename__ = 'votes'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    vote_type: Mapped[int] = mapped_column(Integer, CheckConstraint('vote_type IN (-1, 1)'))


class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime_stamp] = mapped_column(DateTime)


class Reply(Base):
    __tablename__ = 'replies'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime_stamp] = mapped_column(DateTime)





############################################################################
#                                                                          #
#                               TRADES &                                   #
#                                                                          #
############################################################################
class Trade(Base):
    __tablename__ = 'trades'
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    ticker_id: Mapped[int] = mapped_column(Integer, ForeignKey('tickers.id'))

    status: Mapped[int] = mapped_column(Integer, nullable=False)
    cursor: Mapped[date_stamp] = mapped_column(Date, nullable=True)
    strategy: Mapped[str] = mapped_column(String(3), nullable=False)

    entry_date: Mapped[date_stamp] = mapped_column(Date, init=False, nullable=True)
    exit_date: Mapped[date_stamp] = mapped_column(Date, init=False, nullable=True)
    entry_price: Mapped[Float] = mapped_column(Float, init=False, nullable=True)
    exit_price: Mapped[Float] = mapped_column(Float, init=False, nullable=True)
    position: Mapped[int] = mapped_column(Integer, init=False, nullable=True)