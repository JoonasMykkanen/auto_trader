# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dev.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:27:42 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/24 06:33:10 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This includes router for testing random stuff

from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi import APIRouter

from ..core.database import db_dependency
from ..core.config import logger
from ..core.models import User

from ..services.security import authenticate_token
from ..services.crud.candles import *
from ..services.strategies.qullamaggie import *
from ..services.crud.tickers import *
from ..services.crud.candles import *
from ..services.weekly_candle import *
from ..services.daily_candle import *
from ..services.indices import *

from typing import Annotated
from fastapi import Depends

# TODO: TESTING
# from threading import Lock
# import concurrent.futures

test_router = APIRouter()

@test_router.get('/')
def listen_root(user: Annotated[User, Depends(authenticate_token)]):
    try:
        logger.info(f'/test/root called: {user}')
        return "authenticated"

    except Exception as error:
        logger.exception(f'Exception bottom found -> did not catch above: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


@test_router.get('/spx')
def listen_spx(db: db_dependency):
    try:
        logger.info('/test/spx called')
        data = fetch_spx_tickers()
        create_tickers(data, db)
        logger.info(f'saved {len(data)} tickers to database')
        return f'saved {len(data)} tickers to database'

    except Exception as error:
        return f'{error}'
    


@test_router.get('/spx-data')
def listen_data(db: db_dependency):
    try:
        tickers = read_spx_tickers(db)
    
        records_sum = 0
        for ticker in tickers:
            candles = fetch_daily_candles(ticker, db)
            create_candles(candles, db)
            logger.info(f'saved {len(candles)} records for ticker: {ticker.name}')
            records_sum += len(candles)
        for ticker in tickers:
            candles = fetch_weekly_candles(ticker, db)
            create_candles(candles, db)
        return f"all tickers ok - total of {records_sum} candles saved -> thats a whopping {records_sum * 5} data points!!"

    except Exception as error:
        logger.error(error)
        return f'{error}'



@test_router.get('/kulla', response_class=HTMLResponse)
def test_strat(db: db_dependency):
    try:
        # tickers = read_spx_tickers(db)
        # for ticker in tickers:
            # logger.debug(f'testing for: {ticker.name}')
        ticker = read_ticker('AAPL', db)
        data = backtest_qullamaggie(ticker, db)
        logger.debug('\n\n\n')
        return f'{data}'

    except Exception as error:
        logger.error(error)
        return f'{error}'

