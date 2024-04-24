# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dev.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:27:42 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 08:33:38 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This includes router for testing random stuff

from fastapi import APIRouter

from ..services.candle import fetch_daily
from ..services.crud import save_candles
from ..core.config import logger
from ..core.config import config

test_router = APIRouter()

@test_router.get('/')
def listen_root():
    try:
        logger.info('/test/root called')
        data = fetch_daily('AAPL', config.DAILY)
        save_candles(data)
        return data
    except Exception as error:
        logger.exception(error)