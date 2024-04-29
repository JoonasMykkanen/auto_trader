# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:07:21 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 18:25:09 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: https://foss.heptapod.net/python-libs/passlib/-/issues/190
# TODO: Update passlib to 1.7.5 when relases to make sure it's compitable with bcrypt
# TODO: upgrade bcrypt to newer version when supported

from .crud.users import read_user_by_email
from ..core.database import db_dependency
from passlib.context import CryptContext
from ..core.models import User
from ..core.error import *
from ..core.config import logger


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
    min_verify_time='1s',
    bcrypt__rounds=15,
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def authenticate_user(db: db_dependency, email: str, password: str) -> User:
    """ get user from db if username and password ok """
    user = read_user_by_email(db, email)
    logger.debug(user)
    if not user:
        raise WrongEmailError('Invalid email, no such user')
    if not verify_password(password, user.hash):
        raise WrongPasswordError('Wrong password')
    return user


