# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/20 05:56:00 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/21 08:33:50 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dotenv import load_dotenv
import os

load_dotenv()
print("config started")

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')


config = Config()