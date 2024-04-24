# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    database.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 08:19:40 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/23 07:59:29 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import config

engine = create_engine(config.DATABASE_URL)

Session = sessionmaker(bind=engine)

session = Session()