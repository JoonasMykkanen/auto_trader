# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    indices.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/24 15:48:35 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/26 08:41:20 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: Could break at any given time if Wikipedia changes layout or HTML structure

from ..core.config import config
from ..core.config import logger
from ..core.models import Ticker
from bs4 import NavigableString
from bs4 import BeautifulSoup
from typing import List
# from
import requests


def find_table(url: str) -> NavigableString | None:
    """ Retrieves table from wikipedia url """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    return table


def parse_tickers(table: NavigableString) -> List[Ticker]:
    """ Parses given table to retrieve ticker names """
    tickers = []
    for row in table.findAll('tr')[1:]:
        name = row.findAll('td')[0].text[:-1]
        ticker = Ticker(name=name, index=config.SPX)
        tickers.append(ticker)
    return tickers


def fetch_spx_tickers() -> List[Ticker]:
    try:
        table = find_table(config.SPX_URL)
        if table is None:
            raise TypeError('Expected bs4 table, recieved None')
        tickers = parse_tickers(table)
        return tickers

    except Exception as error:
        logger.error(error)
        return None


def fetch_dow_tickers() -> List[Ticker]:
    try:
        table = find_table(config.DJI_URL)

    except Exception as error:
        logger.error(error)
        return None