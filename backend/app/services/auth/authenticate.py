# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    authenticate.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:07:21 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 12:26:17 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from .password import verify_password
from ..crud.users import read_user
from ...core.models import User


def authenticate_user(db: db_dependency, username: str, password: str) -> User | bool:
    """ get user from db if username and password ok """
    user = read_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hash):
        return False
    return user



# https://www.youtube.com/watch?v=NuyzuNBFWxQ&ab_channel=Fireship