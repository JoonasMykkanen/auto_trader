# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/20 05:56:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/23 07:45:23 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dotenv import load_dotenv
from os import getenv
import logging
import sys

# --------------------- ENVIRONMENT ---------------------
load_dotenv()

class Config:
    DAILY = 1
    WEEKLY = 2

    DATABASE_PASSWORD = getenv('DATABASE_PASSWORD')
    DATABASE_USER = getenv('DATABASE_USER')
    DATABASE_URL = getenv('DATABASE_URL')

config = Config()


# --------------------- LOGGING ---------------------
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('backend.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(funcName)s():%(lineno)d - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
