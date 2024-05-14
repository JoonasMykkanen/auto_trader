# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    candles.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:16:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 08:47:52 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import WeeklyCandle
from ...core.models import WeeklyCandle
from ...core.models import DailyCandle
from ...core.models import Ticker

from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy import asc

from datetime import timedelta
from datetime import datetime
from datetime import date
from typing import List


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


def read_daily_candle_latest(ticker: Ticker, db: db_dependency) -> datetime:
    """ retrieve the latest date from __daily_candles__ table or 1.1.1981 """
    # TODO: comment sql statement
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
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
                .filter_by(ticker_id=ticker.id) \
                .order_by(desc(DailyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_daily_candles_since(ticker: Ticker, since: date, db: db_dependency) -> List[DailyCandle]:
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(DailyCandle.date>=since) \
                .order_by(asc(DailyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_weekly_candles_since(ticker: Ticker, since: date, db: db_dependency) -> List[WeeklyCandle]:
    statement = select(WeeklyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(WeeklyCandle.date>=since) \
                .order_by(asc(WeeklyCandle.date))
    candles = db.scalars(statement).all()
    return candles