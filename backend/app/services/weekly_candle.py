# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weekly_candle.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/26 16:24:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 16:35:27 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from .crud.candles import read_all_daily_candles
from ..core.database import db_dependency
from ..core.models import WeeklyCandle
from ..core.models import DailyCandle
from ..core.config import logger
from ..core.models import Ticker
from datetime import timedelta
from typing import List
from math import inf

# TODO: TEST THIS MODULE

def create_weekly_candle(dailies: List[DailyCandle]) -> WeeklyCandle:
    new_open = dailies[0].open
    new_high = -inf
    new_low = inf
    new_close = dailies[-1].close
    new_date = dailies[-1].close
    new_ticker = dailies[-1].close
    new_volume = 0

    for entry in dailies:
        new_high = max(new_high, entry.high)
        new_low = min(new_low, entry.low)
        new_volume += entry.volume

    new_candle = WeeklyCandle(
        date=new_date,
        open=new_open,
        high=new_high,
        low=new_low,
        close=new_close,
        volume=new_volume,
        ticker_id=new_ticker
    )
    return new_candle
        

def fetch_weekly_candles(ticker: Ticker, db: db_dependency) -> List[WeeklyCandle]:
    """ Iterates over the list of dailies and creates weekly candle from daily values """
    try:
        daily_candles = read_all_daily_candles(ticker, db)

        index = 0
        weeklies = []
        while index < len(daily_candles):
            start = daily_candles[index].date - start.weekday()
            end = start + timedelta(days=6)

            dailies = []
            while daily_candles[index].date <= end:
                dailies.append(daily_candles[index])
                index += 1

            candle = create_weekly_candle(dailies)
            weeklies.append(candle)
        return weeklies
    
    except Exception as error:
        logger.exception(error)
        return None
    
    