# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    candle.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:52:25 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 09:12:48 by jmykkane         ###   ########.fr        #
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


from ..core.models import DailyCandle
from ..core.models import Ticker

from ..core.database import session
from ..core.config import logger

from .crud import get_ticker_id
from .tor import tor_request

from datetime import datetime



def build_url(ticker: str, start_date: datetime, end_date: datetime, interval: str):
    """ Creates url to request data from \n\n - ticker: 'AAPL' or other valid ticker name \n\n - interval: '1d' or '1w """
    url = \
        BASE_URL + \
        f'{ticker}?' + \
        f'period1={int(start_date.timestamp())}' + \
        f'&period2={int(end_date.timestamp())}' + \
        END_URL
    return url


def create_candle(data: list[str], ticker_id: int):
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
    


def fetch_daily(ticker: str, mode: int):
    """ Parameters: \n\n - ticker: 'AAPL' \n\n - mode: 1 == daily OR 2 == weekly """
    # TODO: add logic to fetch only dates that are not in the database already
    try:
        url = build_url(ticker, datetime(1981, 1, 1), datetime.now(), '1d')
        response = tor_request(url).text.split('\n')
        ticker_id = get_ticker_id(ticker)

        candles = []
        for line in response[1:]:
            data = line.split(',')
            candles.append(create_candle(data, ticker_id))
        
        return candles
        
    except Exception as error:
        logger.exception(error)