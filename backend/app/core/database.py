# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    database.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 08:19:40 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/23 08:29:36 by jmykkane         ###   ########.fr        #
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
    """ yields local session object and closes connection when done \n\n (directly from fastapi documentation)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]