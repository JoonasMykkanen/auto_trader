# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    users.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:24:38 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 17:44:41 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import User
from ...core.config import config
from ...core.config import logger
from sqlalchemy import select



def read_user_by_email(db: db_dependency, email: str) -> User:
    """ retrieves user from database based on username """
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
