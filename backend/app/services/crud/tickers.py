# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tickers.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:15:17 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/08 19:00:26 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import Ticker
from ...core.config import config
from sqlalchemy import select
from typing import List


def create_ticker(ticker: Ticker, db: db_dependency) -> Ticker:
    """ INSERT INTO tickers ( name, index ) VALUES ( 'AAPL', 'SP500' ); \n\n Push single ticker to db """
    try:
        db.add(ticker)
        db.commit()
        return ticker
    except:
        db.rollback()
        raise


def create_tickers(tickers: List[Ticker], db: db_dependency) -> List[Ticker]:
    """ Push list of tickers to db """
    # TODO: comment sql statement
    try:
        for ticker in tickers:
            db.add(ticker)
        db.commit()
        return tickers
    except:
        db.rollback()
        raise


def read_spx_tickers(db: db_dependency) -> List[Ticker]:
    """ SELECT * FROM tickers WHERE index = 'spx'; \n\n Returns all spx tickers """
    statement = select(Ticker).filter_by(index=config.SPX)
    tickers = db.scalars(statement).all()
    return tickers


def read_ticker(ticker_name: str, db: db_dependency) -> int:
    """ SELECT ticker_name FROM tickers WHERE name = 'AAPL'; \n\n retrieves id for given ticker in db """
    statement = select(Ticker).filter_by(name=ticker_name)
    ticker = db.scalars(statement).first()
    return ticker
