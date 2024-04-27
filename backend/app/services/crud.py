# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crud.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:55:49 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/27 12:35:39 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: using session.rollback() is purely crud.py functions responsibility and will not be handled else where


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
from sqlalchemy import desc
from typing import List


# -------------------- TICKER --------------------

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
    

def read_spx_tickers(db: db_dependency) -> List[Ticker]:
    """ SELECT * FROM tickers WHERE index = 'spx'; \n\n Returns all spx tickers """
    return db.query(Ticker).filter(Ticker.index == config.SPX).all()


# TODO: convert to work with local session
def read_ticker_id(ticker_name: str, db: db_dependency) -> int:
    """ SELECT ticker_name FROM tickers WHERE name = 'AAPL'; \n\n retrieves id for given ticker in db """
    return db.query(Ticker).filter(Ticker.name == ticker_name).first()
        


# -------------------- CANDLE --------------------
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


def read_all_daily_candles(ticker: Ticker, db: db_dependency) -> List[DailyCandle]:
    """ retrieve all daily candles for given ticker """
    # TODO: comment sql statement
    try:
        candles = db.query(DailyCandle) \
                .filter(DailyCandle.ticker_id == ticker.id) \
                .order_by(desc(DailyCandle.date)).all()
        
        if candles == None:
            raise NoResultFound('Absolutely zero(0) tickers found -> run /test/spx to get tickers')
            # TODO: modify path to correct one when implemented
        else:
            return candles
    
    except:
        raise



def read_daily_candle_latest(ticker: Ticker, db: db_dependency) -> datetime:
    """ retrieve the latest date from __daily_candles__ table or 1.1.1981 """
    # TODO: comment sql statement
    try:
        candle = db.query(DailyCandle) \
                .filter(DailyCandle.ticker_id == ticker.id) \
                .order_by(desc(DailyCandle.date)).first()
        if candle == None:
            return datetime(1981, 1, 1)
        else:
            return candle.date + timedelta(days=1)
            
    except:
        raise

