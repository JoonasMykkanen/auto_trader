# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    users.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:24:38 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 07:25:24 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import User
from ...core.config import config
from ...core.config import logger
from sqlalchemy import select
from sqlalchemy import update



def read_user_by_email(db: db_dependency, email: str) -> User:
    statement = select(User).filter_by(email=email)
    user = db.scalars(statement).first()
    return user


def create_user(db: db_dependency, new_user: User) -> User:
    try:
        db.add(new_user)
        db.commit()
    except Exception as error:
        logger.error(f'Could not create new user: {error}')
        db.rollback()
        raise


def reset_user_monthly_voted(db: db_dependency) -> bool:
    try:
        statement = update(User).values(User.voted==False)
        result = db.execute(statement)
        logger.info(f'updated users __voted__ for {result.rowcount} rows')
        return True
    except Exception as error:
        logger.error(f'Could not update users: {error}')
        db.rollback()
        raise