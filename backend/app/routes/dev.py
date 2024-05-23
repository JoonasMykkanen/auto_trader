# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dev.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:27:42 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/15 08:35:33 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This includes router for testing random stuff

from fastapi import APIRouter

from ..core.config import logger
from ..core.models import User
from fastapi import HTTPException
from ..services.security import authenticate_token

from ..services.crud.candles import *
from ..services.crud.tickers import *
from ..services.crud.candles import *
from ..services.indices import *
from ..services.daily_candle import *
from typing import Annotated
from ..services.strategies.qullamaggie import *
from ..services.weekly_candle import *
from ..core.database import db_dependency
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
        
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # url = { executor.submit(ticker_worker, ticker): ticker for ticker in tickers }

        # """
        # for ticker in tickers:
        #     candles = fetch_daily_candles(ticker, db)
        #     create_candles(candles, db)
        #     logger.info(f'saved {len(candles)} records for ticker: {ticker.name}')
        # """
        for ticker in tickers:
            candles = fetch_weekly_candles(ticker, db)
            create_candles(candles, db)
        return "all tickers ok"

    except Exception as error:
        logger.error(error)
        return f'{error}'



@test_router.get('/kulla')
def test_strat(db: db_dependency):
    try:
        tickers = read_spx_tickers(db)
        for ticker in tickers:
            logger.debug(f'testing for: {ticker.name}')
            backtest_qullamaggie(ticker, db)
        logger.debug('\n\n\n')

    except Exception as error:
        logger.error(error)
        return f'{error}'

