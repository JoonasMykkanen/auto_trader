# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/20 05:56:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/24 13:21:02 by jmykkane         ###   ########.fr        #
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
    DATABASE_DB = getenv('POSTGERS_DB')
    DATABASE_PASSWORD = getenv('POSTGRES_USER')
    DATABASE_USER = getenv('POSTGRES_PASSWORD')
    DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgres/{DATABASE_DB}'

    JWT_SECRET = getenv('JWT_SECRET')

    SPX_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    SPX = 'SPX'

    # NOTE: Each strategy has identifying three (3) letter name
    STRATEGY_QUL = 'QUL'


config = Config()


# --------------------- LOGGING ---------------------
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
logger.propagate = False

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('backend.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
