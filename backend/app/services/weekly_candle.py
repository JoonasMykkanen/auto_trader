# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weekly_candle.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/26 16:24:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/26 18:12:58 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.crud import read_all_daily_candles
from ..core.models import WeeklyCandle
from ..core.models import DailyCandle
from ..core.config import logger
from ..core.models import Ticker
from typing import List






def fetch_weekly_candles(ticker: Ticker) -> List[WeeklyCandle]:
    try:
        daily_candles = read_all_daily_candles(ticker)
        

    except Exception as error:
        logger.exception(error)
        return None
    
    