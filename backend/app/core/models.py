# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    models.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:56:01 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/30 15:07:07 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import date as date_stamp
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float

from .config import config
from .config import logger

class Base(DeclarativeBase):
    pass



############################################################################
#                                                                          #
#                              TICKER DATA                                 #
#                                                                          #
############################################################################
class Ticker(Base):
    """ Entrty from 'tickers' table in db \n\n id: serial id \n\n name: AAPL or NVDA \n\n index: SP500 or DOW """
    __tablename__ = 'tickers'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(10), unique=True)
    index: Mapped[str] = mapped_column(String(50), nullable=False)
    company: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'id: {self.id!r}, name: {self.name!r}, index: {self.index!r}'
        
class DailyCandle(Base):
    """ Holds candle stick data within -> linked to a specific ticker """
    __tablename__ = 'daily_candles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

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
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Personal info
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    surname: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[date_stamp] = mapped_column(Date)
    # phone: Mapped[str] = mapped_column(String(15), unique=True)

    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash: Mapped[str] = mapped_column(String(60))
    # TYPE (admin, user, superuser, etc...)
    # Register date

    def __repr__(self) -> str:
        return f'name:  {self.firstname} {self.surname} \nbirthdaty:    {self.birthday} \nemail:    {self.email}\npwd_hash: {self.hash}'





############################################################################
#                                                                          #
#                    POSTS / LIKES / COMMENTS / REPLIES                    #
#                                                                          #
############################################################################
class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date_stamp] = mapped_column(Date)
    author: Mapped[str] = mapped_column(String(50))

class Votes(Base):
    __tablename__ = 'votes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    up_votes: Mapped[int] = mapped_column(BigInteger, default=0)
    down_votes: Mapped[int] = mapped_column(BigInteger, default=0)

class Comments(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date_stamp] = mapped_column(Date)

class Replies(Base):
    __tablename__ = 'replies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date_stamp] = mapped_column(Date)
