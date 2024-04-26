# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/20 05:56:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/26 14:09:24 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dotenv import load_dotenv
from os import getenv
import logging
import sys

# --------------------- ENVIRONMENT ---------------------
load_dotenv()

# NOTE: Includes all CONSTANT variables needed by the application
class Config:
    DATABASE_PASSWORD = getenv('DATABASE_PASSWORD')
    DATABASE_USER = getenv('DATABASE_USER')
    DATABASE_URL = getenv('DATABASE_URL')

    SPX_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    SPX = 'SPX'


config = Config()


# --------------------- LOGGING ---------------------
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
logger.propagate = False

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('backend.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(funcName)s():%(lineno)d - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
