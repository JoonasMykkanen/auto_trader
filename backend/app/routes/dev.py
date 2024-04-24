# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dev.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/22 11:27:42 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 11:47:21 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This includes router for testing random stuff

from fastapi import APIRouter

from ..services.candle import fetch_daily
from ..services.crud import save_candles
from ..core.config import logger
from ..core.config import config
import time

test_router = APIRouter()

@test_router.get('/')
def listen_root():
    try:
        logger.info('/test/root called')
        data = fetch_daily('AAPL', config.DAILY)
        start_time = time.perf_counter()
        save_candles(data)
        end_time = time.perf_counter()
        return f'ok - {len(data)} queries saved in {end_time - start_time} seconds'

    except Exception as error:
        logger.exception(error)