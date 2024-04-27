# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    database.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 08:19:40 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/27 12:21:31 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# TODO: Remove debug prints when sure

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from .config import config
from .config import logger


engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """ yields local session object and closes connection when done """
    db = SessionLocal()
    try:
        logger.debug('local session created')
        yield db
    finally:
        logger.debug('local session closed')
        db.close()

logger.debug('database file loaded --> SessionLocal created // create_engine() ran')
db_dependency = Annotated[Session, Depends(get_db)]