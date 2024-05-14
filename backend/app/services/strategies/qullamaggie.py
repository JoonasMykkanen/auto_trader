# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qullamaggie.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/08 18:31:30 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 07:22:34 by jmykkane         ###   ########.fr        #
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
BREAK_EVEN = 4
TRAILING_STOP = 5
EXITED = 6

from ...core.database import db_dependency
from ...core.models import WeeklyCandle
from ...core.models import Ticker
from ...core.config import logger
from ...core.models import Trade

from ..crud.trade import *
from ..crud.candles import *

from datetime import timedelta
from datetime import date
from typing import List

from pprint import pprint


def qullamaggie_detect_driver_move(ticker: Ticker, db: db_dependency) -> Trade | None:
    """ Tries to find a driver move to initiate trade from """
    

    since = date.today() - timedelta(weeks=12)
    logger.debug(f'candles from: {since}')
    candles = read_weekly_candles_since(ticker, since, db)

    pprint(candles)


def qullamaggie(ticker: Ticker, db: db_dependency):
    trade = qullamaggie_detect_driver_move(ticker, db)
    