# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qullamaggie.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/08 18:31:30 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/08 19:12:54 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
NOTE: Implements trading strategy from https://qullamaggie.com/

ENTRY:
    - Risk per position 0.25% - 1.25% of portfolio

STRATEGY:
    1. driver move of > 30% in last 12 weeks
    2. consolidation sideways of 2-8 weeks > 10/20/50 SMA
    3. enter on breakout
    4. stop loss < 1*ATR

EXIT:
    - 3-5 days to sell 20% - 30%
    - stop loss moved to break even
    - the remaining position has a trailing stoploss using the 10/20 moving average
    - exit only if price closes below trail

"""

from ...core.database import db_dependency
from ...core.models import DailyCandle
from ...core.config import logger

from ..crud.candles import read_daily_candles_since
from ..crud.tickers import read_ticker

from datetime import date
from typing import List



def qullamaggie(ticker: str, db: db_dependency):
    """ """
    since = date(2024, 3, 1)
    ticker = read_ticker(ticker, db)
    candles = read_daily_candles_since(ticker, since, db)
    print(candles)