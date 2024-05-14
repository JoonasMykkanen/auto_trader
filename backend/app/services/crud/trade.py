# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    trade.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/09 07:14:27 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 09:46:55 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# TODO: can optimize db so that each trade is not commited, but I first only add them and commit once every
#       ticker has been looped over and then only commit once


from ...core.database import db_dependency
from ...core.models import Trade
from ...core.config import config
from sqlalchemy import select
from typing import List


def create_trade(new_trade: Trade, db: db_dependency) -> Trade:
    try:
        db.add(new_trade)
        db.commit()
        return new_trade
    except:
        db.rollback()
        raise


def update_trade_status(to_update: Trade, db: db_dependency) -> Trade:
    pass


def update_trade_cursor(to_update: Trade, db: db_dependency) -> Trade:
    pass


def delete_trade(to_delete: Trade, db: db_dependency) -> bool:
    pass


def read_trade(ticker_target: str, strategy_target: str, db: db_dependency) -> Trade | None:
    """ Parameters: \n - ticker_target (str): ticker id \n - strategy_target (str): 'QUL' or other three letter strategy name """
    statement = select(Trade).filter(Trade.ticker_id==ticker_target, Trade.strategy==strategy_target)
    trade = db.scalars(statement).first()
    return trade
