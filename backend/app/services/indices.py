# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    indices.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/24 15:48:35 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/24 21:21:14 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..core.config import config
from ..core.config import logger
from ..core.models import Ticker
from bs4 import BeautifulSoup
from typing import List
import requests


# NOTE: Could break at any given time if Wikipedia changes layout or HTML structure
def fetch_spx_tickers() -> List[Ticker] | None:
    """ Uses wikipedia tables to fetch SPX tickers """
    try:
        response = requests.get(config.SPX_URL)        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable sortable'})  
        
        tickers = []
        for row in table.findAll('tr')[1:]:
            name = row.findAll('td')[0].text[:-1]
            ticker = Ticker(name=name, index=config.SPX)
            tickers.append(ticker)
        return tickers

    except Exception as error:
        logger.error(error)
        return None
