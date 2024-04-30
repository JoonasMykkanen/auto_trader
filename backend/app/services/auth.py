# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 09:07:21 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/30 09:44:28 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: https://foss.heptapod.net/python-libs/passlib/-/issues/190
# TODO: Update passlib to 1.7.5 when relases to make sure it's compitable with bcrypt
# TODO: upgrade bcrypt to newer version when supported

from .crud.users import read_user_by_email
from ..core.database import db_dependency
from passlib.context import CryptContext
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from jose import jwt
from jose import JWTError
from ..core.config import logger
from ..core.config import config
from ..core.models import User
from fastapi.security import OAuth2PasswordBearer
from ..core.error import *
from typing import Annotated
from fastapi import Depends
from ..core.schema import TokenData


TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
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
    if not user:
        raise WrongEmailError('Invalid email, no such user')
    if not verify_password(password, user.hash):
        raise WrongPasswordError('Wrong password')
    return user


def authenticate_token(db: db_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise InvalidTokenError
        token_data = TokenData(email=email)
    except JWTError:
        raise InvalidTokenError
    
    user = read_user_by_email(db, token_data.email)
    if user is None:
        InvalidTokenError
    return user


def get_token(user: str) -> str:
    """Taking in username and expiration, returning access token to be used in further requests \n\nParameters:\n\n- data (dict): { sub: __str__, exp: __datetime__ }"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode = { 'sub': user, 'exp': expire }
    jwt_token = jwt.encode(to_encode, config.JWT_SECRET, algorithm=ALGORITHM)
    return jwt_token

