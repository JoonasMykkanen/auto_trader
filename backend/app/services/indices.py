# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    indices.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/24 15:48:35 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/01 07:17:28 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: Could break at any given time if Wikipedia changes layout or HTML structure

from ..core.config import config
from ..core.config import logger
from ..core.models import Ticker
from bs4 import NavigableString
from bs4 import BeautifulSoup
from typing import List
import requests


def find_table(url: str) -> NavigableString | None:
    """ Retrieves table from wikipedia url """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    return table


def fetch_spx_tickers() -> List[Ticker]:
    try:
        table = find_table(config.SPX_URL)
        if table == None:
            raise TypeError('Expected bs4 table, recieved None')
        
        tickers = []
        for row in table.findAll('tr')[1:]:
            name = row.findAll('td')[0].text[:-1]
            company = row.findAll('td')[1].text[:-1]
            ticker = Ticker(
                name=name,
                index=config.SPX,
                company=company
            )
            tickers.append(ticker)
        return tickers

    except Exception as error:
        logger.exception(error)
        return None
