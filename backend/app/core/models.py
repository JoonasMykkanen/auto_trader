# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    models.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:56:01 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 21:21:21 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import String
from .database import engine


class Base(DeclarativeBase):
    pass


class Ticker(Base):
    """ Entrty from 'tickers' table in db \n\n id: serial id \n\n name: AAPL or NVDA \n\n index: SP500 or DOW """
    __tablename__ = 'tickers'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(10), unique=True)
    index: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'id: {self.id!r}, name: {self.name!r}, index: {self.index!r}'
        


class DailyCandle(Base):
    """ Entry from 'daily_candles table in db """
    __tablename__ = 'daily_candles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=True)
    open: Mapped[Float] =  mapped_column(Float, nullable=False)
    high: Mapped[Float] = mapped_column(Float, nullable=False)
    low: Mapped[Float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ticker_id: Mapped[int] = mapped_column(Integer, ForeignKey('tickers.id'))

    

# class WeeklyCandle(Base):
#     """ Entry from 'weekly_candles table in db """
#     __tablename__ = 'weekly_candles'
#     id = mapped_column(Integer, primary_key=True)

#     volume = mapped_column(DECIMAL, nullable=False)
#     open = mapped_column(DECIMAL, nullable=False)
#     close = mapped_column(DECIMAL, nullable=False)
#     high = mapped_column(DECIMAL, nullable=False)
#     low = mapped_column(DECIMAL, nullable=False)
#     date = mapped_column(Date, nullable=False)
#     ticker_id = mapped_column(Integer, ForeignKey('tickers.id'))



Base.metadata.create_all(bind=engine)
