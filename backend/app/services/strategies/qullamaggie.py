# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qullamaggie.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/08 18:31:30 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/23 06:51:33 by jmykkane         ###   ########.fr        #
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


SEARCHING = 0
DRIVER_FOUND = 1
CONSOLIDATION = 2
BREAKOUT = 3
INITIAL_SELL = 4
TRAILING_STOP = 5
EXITED = 6
ABORT = 7

DRIVER_MULTIPLIER = 1.1
RANGE_PRECENTAGE = 5

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



def initialize_trade(ticker: Ticker, avg_volume: int, candle: DailyCandle, db: db_dependency):
    new_trade = Trade(
        ticker_id = ticker.id,
        status = DRIVER_FOUND,
        cursor = candle.date,
        strategy = config.STRATEGY_QUL,
        driver_avg_vol = avg_volume
    )
    return new_trade


def detect_driver_move(ticker: Ticker, today: date, db: db_dependency):
    since = today - timedelta(weeks=12)
    candles = read_weekly_candles_range(ticker, since, today, db)
    threshold = candles[0].close * DRIVER_MULTIPLIER
    if candles[-1].close > threshold:
        return True
    return False




# BACKTESTING

def backtest_qullamaggie(ticker: Ticker, db: db_dependency):
    pass
        
