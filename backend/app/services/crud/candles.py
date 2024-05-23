# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    candles.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:16:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/15 09:31:11 by jmykkane         ###   ########.fr        #
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


def create_candles(candles: List[DailyCandle] | List[WeeklyCandle], db: db_dependency) -> None:
    """ Push list of candles """
    try:
        for candle in candles:
            db.add(candle)
        db.commit()
    except:
        db.rollback()
        raise


def read_daily_candle_latest(ticker: Ticker, db: db_dependency) -> datetime:
    """ retrieve the latest date from __daily_candles__ table or 1.1.1981 """
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
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .order_by(asc(DailyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_daily_candles_date(ticker: Ticker, since: date, db: db_dependency) -> List[DailyCandle]:
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(DailyCandle.date >= since) \
                .order_by(asc(DailyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_daily_candles_price(ticker: Ticker, since: date, db: db_dependency) -> List[DailyCandle]:
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(DailyCandle.date >= since) \
                .order_by(asc(DailyCandle.close))
    candles = db.scalars(statement).all()
    return candles


def read_weekly_candles_since(ticker: Ticker, since: date, db: db_dependency) -> List[WeeklyCandle]:
    statement = select(WeeklyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(WeeklyCandle.date>=since) \
                .order_by(asc(WeeklyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_weekly_candles_range(ticker: Ticker, start: date, end: date, db: db_dependency) -> List[WeeklyCandle]:
    statement = select(WeeklyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(WeeklyCandle.date>=start, WeeklyCandle.date<=end) \
                .order_by(asc(WeeklyCandle.date))
    candles = db.scalars(statement).all()
    return candles


def read_weekly_next(ticker: Ticker, cursor: date, db: db_dependency) -> WeeklyCandle:
    statement = select(WeeklyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(WeeklyCandle.date > cursor) \
                .order_by(asc(WeeklyCandle.date))
    candle = db.scalars(statement).first()
    return candle


def read_daily_next(ticker: Ticker, cursor: date, db: db_dependency) -> DailyCandle:
    statement = select(DailyCandle) \
                .filter_by(ticker_id=ticker.id) \
                .filter(DailyCandle.date > cursor) \
                .order_by(asc(DailyCandle.date))
    candle = db.scalars(statement).first()
    return candle