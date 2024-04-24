# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crud.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:55:49 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 08:33:28 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: using session.rollback() is purely crud.py functions responsibility


# from ..core.models import WeeklyCandle
from ..core.models import DailyCandle
from ..core.database import session
from ..core.models import Ticker
from ..core.config import logger
from sqlalchemy import select
from typing import List


# -------------------- TICKER --------------------

def create_ticker(ticker: Ticker):
    """ INSERT INTO tickers ( name, index ) VALUES ( 'AAPL', 'SP500' ); \n\n Push single ticker to db """
    try:
        session.add(ticker)
        session.commit()
        logger.info(f'record saved for __{ticker.name}__')
    except Exception as error:
        logger.exception(error)
        session.rollback()


def create_tickers(tickers: List[Ticker]):
    """ Push list of tickers to db """
    try:
        for ticker in tickers:
            session.add(ticker)
        session.commit()
        logger.info(f'Saved {len(tickers)} records to table: daily_candles')
    except Exception as error:
        logger.exception(error)
        session.rollback()

 
def get_ticker_id(ticker_name: str):
    """ SELECT name FROM tickers WHERE name = 'AAPL'; \n\n retrieves id for given ticker in db """
    try:
        select_ticker_by_name = select(Ticker).where(Ticker.name == ticker_name)
        result = session.execute(select_ticker_by_name)
        ticker = result.scalars().first()
        logger.info(f'ticker id({ticker.id}) succesfully fetched for __{ticker.name}__')
        return ticker.id
    except Exception as error:
        logger.exception(error)
        session.rollback()
        




# -------------------- CANDLE --------------------
def save_candles(candles: List[DailyCandle]):
    """ Push list of candles """
    try:
        for candle in candles:
            session.add(candle)
        session.commit()
        logger.info(f'Saved {len(candles)} records to table: daily_candles')
    except Exception as error:
        logger.exception(error)
        session.rollback()