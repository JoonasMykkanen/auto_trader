# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dev.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:27:42 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 23:54:04 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This includes router for testing random stuff

from fastapi import APIRouter

from ..services.indices import fetch_spx_tickers
from ..services.crud import read_spx_tickers
from ..services.candle import fetch_daily_candles
from ..services.crud import create_candles
from ..services.crud import create_tickers
from ..core.config import logger
from ..core.config import config
import time

test_router = APIRouter()

# @test_router.get('/')
# def listen_root():
#     try:
#         logger.info('/test/root called')
#         data = fetch_daily('AAPL', config.DAILY)
#         start_time = time.perf_counter()
#         create_candles(data)
#         end_time = time.perf_counter()
#         return f'ok - {len(data)} queries saved in {end_time - start_time} seconds'

#     except Exception as error:
#         logger.exception(error)


@test_router.get('/spx')
def listen_spx():
    try:
        logger.info('/test/spx called')
        data = fetch_spx_tickers()
        create_tickers(data)
        logger.info(f'saved {len(data)} tickers to database')
        return f'saved {len(data)} tickers to database'

    except Exception as error:
        return f'Internal server error'
    

@test_router.get('/spx-data')
def listen_data():
    try:
        tickers = read_spx_tickers()
        
        for ticker in tickers:
            candles = fetch_daily_candles(ticker, config.DAILY)
            create_candles(candles)
            logger.info(f'saved {len(candles)} records for ticker: {ticker.name}')
        
        return "all tickers ok"

    except Exception as error:
        logger.error(error)
        return f'{error}'