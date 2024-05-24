# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qullamaggie.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/08 18:31:30 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/24 13:54:32 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
NOTE: Implements trading strategy from https://qullamaggie.com/

ENTRY:
    - Position size 10% - 20% of portfolio
    - stoploss per position 0.25% - 1.25%

STRATEGY:
    1. driver move of > 30% in last 12 weeks
    2. consolidation sideways of 2-8 weeks > 10/20/50 SMA
    3. enter on breakout
    4. stop loss @ low of the breakout day

EXIT:
    
    - 

"""


SEARCHING = 0
DRIVER_FOUND = 1
CONSOLIDATION = 2
BREAKOUT = 3
INITIAL_SELL = 4
TRAILING_STOP = 5
EXITED = 6
ABORT = 7
TIMEOFF = 8


CONSOLIDATION_MIN = 10
CONSOLIDATION_MAX = 40
ATR_RANGE_PRECENTAGE = 5


from ...core.database import db_dependency
from ...core.config import logger
from ...core.config import config

from ...core.models import WeeklyCandle
from ...core.models import Ticker
from ...core.models import Trade

from ..crud.candles import *
from ..crud.trade import *

from backtesting.lib import crossover
from backtesting import Backtest
from backtesting import Strategy
from pandas import DataFrame
import pandas as pd
import talib

from datetime import timedelta
from datetime import date
from pprint import pprint
from typing import List




#########################
#      BACKTESTING      #  
#########################
consolidation_dates = []
driver_dates = []


def create_df(candles: List[DailyCandle]) -> DataFrame:
    df = pd.DataFrame([{
        'Date': d.date,
        'Open': d.open,
        'High': d.high,
        'Low': d.low,
        'Close': d.close,
        'Volume': d.volume
    } for d in candles])
    df['Date'] = pd.to_datetime(df['Date'])
    # df.set_index('Date', inplace=True)
    return df


class driverMove(Strategy):
    
    def init(self):
        self.roc = self.I(talib.ROC, self.data.Close, 60)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.sma10 = self.I(talib.SMA, self.data.Close, 10, overlay=True)
        self.sma20 = self.I(talib.SMA, self.data.Close, 20, overlay=True)
        self.sma50 = self.I(talib.SMA, self.data.Close, 50, overlay=True)

        self.consolidation_start = None
        self.initial_sell_offset = 3
        self.status = SEARCHING
        self.entry = None
        
    

    def next(self):
        # 1. driver move of > 30% in last 12 weeks
        if self.status == SEARCHING:
            if self.roc[-1] > 30:
                self.consolidation_start = len(self.data.Close) - 1
                self.status = DRIVER_FOUND

        elif self.status == DRIVER_FOUND:
            current_index = len(self.data.Close) - 1
            consolidation_period = current_index - self.consolidation_start
            if consolidation_period < CONSOLIDATION_MIN:
                # atr = self.atr * ATR_RANGE_PRECENTAGE / 100
                if self.data.Close[current_index] > self.data.Close[self.consolidation_start]:
                    self.consolidation_start = current_index
            else:
                self.status = CONSOLIDATION
        
        # 2. consolidation sideways of 2-8 weeks > 10/20/50 SMA
        # 3. enter on breakout
        # 4. stop loss @ low of the breakout day
        elif self.status == CONSOLIDATION:
            current_index = len(self.data.Close) - 1
            if crossover(self.sma20, self.data.Close):
                self.status = SEARCHING
                return
            consolidation_period = current_index - self.consolidation_start
            price_range = self.data.High[self.consolidation_start:current_index]
            top = price_range.max()
            # NOTE: use volume as indicator for break out
            breakout_threshold = self.data.Close[self.consolidation_start] * (1 + self.atr * 5 / 100)
            if self.data.Close[current_index] > breakout_threshold:
                logger.debug(f'breakout @ {current_index} roc: {self.roc[self.consolidation_start]} after {len(price_range)} consolidation days')
                stop_loss = self.data.Low[current_index] - self.atr[current_index]
                self.buy(sl=stop_loss, size=1000)
                logger.debug(f'stop loss @ {stop_loss}')
                self.entry_index = current_index
                self.status = BREAKOUT
        
        # 5. 3-5 days to sell 20% - 30% && move stop loss to entry price
        #    move stoploss to break even or entry price
        elif self.status == BREAKOUT:
            if len(self.orders) == 0 and self.position.size == 0:
                self.position.close()
                self.status = SEARCHING
                return
            current_index = len(self.data.Close) - 1
            delta = current_index - self.entry_index
            if delta < self.initial_sell_offset:
                return
            self.position.close(0.3)
            current_trade = self.trades[0]
            current_trade.sl = current_trade.entry_price
            logger.debug(f'stop loss set to: {current_trade.sl}')
            logger.debug(f'currently open: {self.position.size}')
            self.status = TRAILING_STOP
            logger.debug(f'INITIAL SELL')
        
        # 6. the remaining position has a trailing stoploss using the 10/20 moving average
        #    exit only if price closes below trail
        elif self.status == TRAILING_STOP:
            if crossover(self.sma20, self.data.Close):
                self.position.close()
                self.status = SEARCHING
                logger.debug(f'POSITION CLOSED')


            

            
def backtest_qullamaggie(ticker: Ticker, db: db_dependency):
    daily_candles = read_all_daily_candles(ticker, db)
    daily_df = create_df(daily_candles)
    bt = Backtest(
        cash = 10000,
        data = daily_df,
        strategy = driverMove,
        trade_on_close = True,
        exclusive_orders = True,
        )

    
    output = bt.run()
    logger.debug(output)
    bt.plot()
    with open('driverMove.html') as file:
        data = file.read()
        file.close()
        return data
    logger.info(output)
    