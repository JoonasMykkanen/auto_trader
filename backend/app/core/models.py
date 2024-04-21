# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    models.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:56:01 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/21 08:17:16 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import DECIMAL
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Date


Base = declarative_base()

class Ticker(Base):
    """ Entrty from 'tickers' table in db \n\n id: serial id \n\n name: AAPL or NVDA \n\n index: SP500 or DOW """
    __tablename__ = 'tickers'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    index = Column(String(50), nullable=False)


class DailyCandle(Base):
    """ Entry from 'daily_candles table in db """
    __tablename__ = 'daily_candles'

    id = Column(Integer, primary_key=True)
    volume = Column(DECIMAL, nullable=False)
    open = Column(DECIMAL, nullable=False)
    close = Column(DECIMAL, nullable=False)
    high = Column(DECIMAL, nullable=False)
    low = Column(DECIMAL, nullable=False)
    date = Column(Date, nullable=False)
    ticker_id = Column(Integer, ForeignKey('tickers.ticker_id'))
    

class WeeklyCandle(Base):
    """ Entry from 'weekly_candles table in db """
    __tablename__ = 'daily_candles'

    id = Column(Integer, primary_key=True)
    volume = Column(DECIMAL, nullable=False)
    open = Column(DECIMAL, nullable=False)
    close = Column(DECIMAL, nullable=False)
    high = Column(DECIMAL, nullable=False)
    low = Column(DECIMAL, nullable=False)
    date = Column(Date, nullable=False)
    ticker_id = Column(Integer, ForeignKey('tickers.ticker_id'))
