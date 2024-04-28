# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    models.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:56:01 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 07:02:40 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# TODO: Make all String(N) fields as small as possible to save disk space (before going live ofc -> not for MVP)



from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from datetime import datetime
from .config import logger

from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import String



class Base(DeclarativeBase):
    pass


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

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
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

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    open: Mapped[Float] =  mapped_column(Float, nullable=False)
    high: Mapped[Float] = mapped_column(Float, nullable=False)
    low: Mapped[Float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ticker_id: Mapped[int] = mapped_column(Integer, ForeignKey('tickers.id'))

    __table_args__  = (UniqueConstraint('date', 'ticker_id', name='date_weekly_uc'),)



class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Personal info
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True)

    # User info
    username: Mapped[str] = mapped_column(String())
    # hash: Mapped[str] = mapped_column(String())
    # salt: Mapped[str] = mapped_column(String())







# class Wallet(Base):
#     __tablename__ = 'wallets'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

# class Post(Base):
#     __tablename__ = 'posts'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
