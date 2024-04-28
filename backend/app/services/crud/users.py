# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    users.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:24:38 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 09:27:54 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import User
from ...core.config import config
from ...core.config import logger
from datetime import timedelta
from datetime import datetime
from sqlalchemy import select
from sqlalchemy import desc
from typing import List


def read_user(db: db_dependency, username: str) -> User:
    """ retrieves user from database based on username """
    statement = select(User).filter_by(username=username)
    user = db.scalars(statement).first()
    return user