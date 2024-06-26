# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    daily_candle.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:52:25 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 16:35:13 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Module contains logic to fetch any given ticker in any given interval from Yahoo Finance
# NOTE --> period1 & period2 follows Unix timestamp convention (seconds since 1.1.1970)

# NOTE: Current implementation can break at any given time if Yahoo changes their API conventions
# NOTE: Below example of correct url format (as of 22.04.2024)
# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=347155200&period2=1713267290&interval=1d&events=history&includeAdjustedClose=true
# BASE + TICKER + PERIOD + INTERVAL + END

BASE_URL = 'https://query1.finance.yahoo.com/v7/finance/download/'
END_URL = '&events=history&includeAdjustedClose=true'

DAILY = 1
WEEKLY = 2


from ..core.database import db_dependency
from ..core.models import DailyCandle
from ..core.models import Ticker
from ..core.config import logger

from .crud.candles import read_daily_candle_latest
from .tor import tor_request

from datetime import datetime
from typing import List


def build_url(ticker: str, start_date: datetime, end_date: datetime, interval: str) -> str:
    """ Creates url to request data from \n\n - ticker: 'AAPL' or other valid ticker name \n\n - interval: '1d' or '1w """
    url = \
        BASE_URL + \
        f'{ticker}?' + \
        f'period1={int(start_date.timestamp())}' + \
        f'&period2={int(end_date.timestamp())}' + \
        END_URL
    return url


def create_candle(data: list[str], ticker_id: int) -> DailyCandle:
    """ Parses one line from response to a ticker object \n\n INFO:     Date,Open,High,Low,Close,Adj Close,Volume """
    return DailyCandle(
                date = datetime.strptime(data[0], '%Y-%m-%d'),
                open = float(data[1]),
                high = float(data[2]),
                low = float(data[3]),
                close = float(data[4]),
                volume = int(data[6]),
                ticker_id = ticker_id
            )


def fetch_daily_candles(ticker: Ticker, db: db_dependency) -> List[DailyCandle] | None:
    """ Gets daily candlestick data for given ticker from 1981 or latest saved in database up until datetime.now() \n\n Parameters: \n\n - ticker: 'AAPL'"""
    try:
        start_date = read_daily_candle_latest(ticker, db)
        url = build_url(ticker.name, start_date, datetime.now(), '1d')
        response = tor_request(url).text.split('\n')

        candles = []
        for line in response[1:]:
            data = line.split(',')
            candle = create_candle(data, ticker.id)
            candles.append(candle)
        
        return candles
        
    except Exception as error:
        logger.exception(error)
        return None