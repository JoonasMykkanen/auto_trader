# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crud.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:55:49 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/25 16:01:23 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: using session.rollback() is purely crud.py functions responsibility and will not be handled else where


# from ..core.models import WeeklyCandle
from sqlalchemy.exc import IntegrityError
from ..core.models import DailyCandle
from ..core.database import session
from ..core.models import Ticker
from ..core.config import config
from ..core.config import logger
from datetime import timedelta
from sqlalchemy import select
from datetime import datetime
from sqlalchemy import desc
from typing import List


# -------------------- TICKER --------------------

def create_ticker(ticker: Ticker) -> Ticker:
    """ INSERT INTO tickers ( name, index ) VALUES ( 'AAPL', 'SP500' ); \n\n Push single ticker to db """
    try:
        session.add(ticker)
        session.commit()
        return ticker
    except Exception as error:
        logger.exception(error)
        session.rollback()
        return None


def create_tickers(tickers: List[Ticker]) -> List[Ticker]:
    """ Push list of tickers to db """
    try:
        for ticker in tickers:
            session.add(ticker)
        session.commit()
        return tickers
    except Exception as error:
        logger.exception(error)
        session.rollback()
        return None
    

def read_spx_tickers() -> List[Ticker]:
    """ Returns all spx tickers """
    try:
        select_spx_tickers = select(Ticker).where(Ticker.index == config.SPX)
        result = session.execute(select_spx_tickers)
        tickers = result.scalars().all()
        return tickers
    except Exception as error:
        logger.exception(error)
        return None

 
def read_ticker_id(ticker_name: str) -> int:
    """ SELECT name FROM tickers WHERE name = 'AAPL'; \n\n retrieves id for given ticker in db """
    try:
        select_ticker_by_name = select(Ticker).where(Ticker.name == ticker_name)
        result = session.execute(select_ticker_by_name)
        ticker = result.scalars().first()
        return ticker.id
    except Exception as error:
        logger.exception(error)
        # session.rollback()
        # TODO: figure out if needed
        return None
        




# -------------------- CANDLE --------------------
def create_candles(candles: List[DailyCandle]) -> List[DailyCandle]:
    """ Push list of candles """
    try:
        for candle in candles:
            session.add(candle)
        session.commit()
        return candles
    except Exception as error:
        logger.exception(error)
        session.rollback()
        return None



def read_daily_candle_latest(ticker: Ticker) -> datetime:
    """ retrieve the latest date from __daily_candles__ table or 1.1.1981 """
    try:
        candle = session.query(DailyCandle) \
                .filter(DailyCandle.ticker_id == ticker.id) \
                .order_by(desc(DailyCandle.date)).first()
        if candle is not None:
            return candle.date + timedelta(days=1)
        else:
            return datetime(1981, 1, 1)
            
    except Exception as error:
        logger.exception(error)
        # session.rollback()
        # TODO: figure out if needed
        # TODO: Raise some error and catch @ caller