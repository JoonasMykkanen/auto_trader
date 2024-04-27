# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crud.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:55:49 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/27 13:26:18 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# TODO: change queries to comply: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying

from ..core.database import db_dependency
from ..core.models import WeeklyCandle
from ..core.models import WeeklyCandle
from ..core.models import DailyCandle
from ..core.models import Ticker
from ..core.config import config
from sqlalchemy.exc import NoResultFound
from ..core.config import logger
from datetime import timedelta
from datetime import datetime
from sqlalchemy import select
from sqlalchemy import desc
from typing import List


# ------------------------------ CREATE ------------------------------ #
def create_ticker(ticker: Ticker, db: db_dependency) -> Ticker:
    """ INSERT INTO tickers ( name, index ) VALUES ( 'AAPL', 'SP500' ); \n\n Push single ticker to db """
    try:
        db.add(ticker)
        db.commit()
        return ticker
    except:
        db.rollback()
        raise


def create_tickers(tickers: List[Ticker], db: db_dependency) -> List[Ticker]:
    """ Push list of tickers to db """
    # TODO: comment sql statement
    try:
        for ticker in tickers:
            db.add(ticker)
        db.commit()
        return tickers
    except:
        db.rollback()
        raise


def create_daily_candles(candles: List[DailyCandle] | List[WeeklyCandle], db: db_dependency) -> None:
    """ Push list of candles """
    # TODO: comment sql statement
    try:
        for candle in candles:
            db.add(candle)
        db.commit()
    except:
        db.rollback()
        raise





# ------------------------------ READ ------------------------------ #
def read_spx_tickers(db: db_dependency) -> List[Ticker]:
    """ SELECT * FROM tickers WHERE index = 'spx'; \n\n Returns all spx tickers """
    statement = select(Ticker).where(Ticker.name == config.SPX)
    tickers = db.scalars().all()
    return tickers


def read_ticker_id(ticker_name: str, db: db_dependency) -> int:
    """ SELECT ticker_name FROM tickers WHERE name = 'AAPL'; \n\n retrieves id for given ticker in db """
    statement = select(Ticker).where(Ticker.name == ticker_name)
    ticker = db.scalars(statement).first()
    return ticker


def read_daily_candle_latest(ticker: Ticker, db: db_dependency) -> datetime:
    """ retrieve the latest date from __daily_candles__ table or 1.1.1981 """
    # TODO: comment sql statement
    statement = select(DailyCandle) \
                .where(DailyCandle.ticker_id == ticker.id) \
                .order_by(desc(DailyCandle.date))

    candle = db.scalars(statement).first()    
    if candle == None:
        return datetime(1981, 1, 1)
    else:
        return candle.date + timedelta(days=1)


def read_all_daily_candles(ticker: Ticker, db: db_dependency) -> List[DailyCandle]:
    """ retrieve all daily candles for given ticker """
    # TODO: comment sql statement
    statement = select(DailyCandle) \
                .where(DailyCandle.ticker_id == ticker.id) \
                .order_by(desc(DailyCandle.date))

    candles = db.scalars(statement).all()
    return candles
        


# ------------------------------ UPDATE ------------------------------ #



# ------------------------------ DELETE ------------------------------ #