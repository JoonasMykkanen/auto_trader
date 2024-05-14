# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qullamaggie.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/08 18:31:30 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 09:50:15 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
NOTE: Implements trading strategy from https://qullamaggie.com/

ENTRY:
    - Position size 10% - 20% of portfolio
    - stoploss per position 0.25% - 1.25%

STRATEGY:
    1. driver move of > 30% in last 12 weeks
    2. consolidation sideways of 2-8 weeks > 10/20/50 SMA
    3. enter on breakout
    4. stop loss @ low of the breakout day

EXIT:
    - 3-5 days to sell 20% - 30% && move stop loss to entry price
    - the remaining position has a trailing stoploss using the 10/20 moving average
    - exit only if price closes below trail

"""

DRIVER_FOUND = 1
CONSOLIDATION = 2
BREAKOUT = 3
INITIAL_SELL = 4
TRAILING_STOP = 5
EXITED = 6

DRIVER_MULTIPLIER = 1.1

from ...core.database import db_dependency
from ...core.config import logger
from ...core.config import config

from ...core.models import WeeklyCandle
from ...core.models import Ticker
from ...core.models import Trade

from ..crud.candles import *
from ..crud.trade import *

from datetime import timedelta
from datetime import date
from pprint import pprint
from typing import List



def initialize_trade(ticker: Ticker, candle: DailyCandle, db: db_dependency):
    new_trade = Trade(
        ticker_id = ticker.id,
        status = DRIVER_FOUND,
        cursor = candle.date,
        strategy = config.STRATEGY_QUL,
    )
    create_trade(new_trade, db)
    return new_trade


# DRIVER_FOUND
def detect_driver_move(ticker: Ticker, db: db_dependency) -> Trade | None:
    since = date.today() - timedelta(weeks=12)
    candles = read_daily_candles_since(ticker, since, db)
    start = candles[0]
    threshold = start.close * DRIVER_MULTIPLIER
    for candle in candles:
        current = candle
        if current.close >= threshold:
            print(f'FOUND: {current}')
            new_trade = initialize_trade(ticker, current, db)
            logger.debug(f'FOUND trade on {new_trade}')
            return new_trade
    logger.debug('no entry found in detect_driver_move')
    return None



def qullamaggie(ticker: Ticker, db: db_dependency):
    trade = read_trade(ticker.id, config.STRATEGY_QUL, db)
    if not trade:
        logger.debug('no trade found on db')
        detect_driver_move(ticker, db)
    elif trade.status == DRIVER_FOUND:
        pass
    elif trade.status == CONSOLIDATION:
        pass
    elif trade.status == BREAKOUT:
        pass
    elif trade.status == INITIAL_SELL:
        pass
    elif trade.status == TRAILING_STOP:
        pass
    elif trade.status == EXITED:
        pass