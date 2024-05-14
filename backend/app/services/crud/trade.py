# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    trade.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/09 07:14:27 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 06:58:26 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import Ticker
from ...core.models import Trade
from ...core.config import config
from sqlalchemy import select
from typing import List


def create_trade(trade: Trade, db: db_dependency) -> Trade:
    pass


def update_trade(to_update: Trade, db: db_dependency) -> Trade:
    pass


def delete_trade(to_delete: Trade, db: db_dependency) -> bool:
    pass