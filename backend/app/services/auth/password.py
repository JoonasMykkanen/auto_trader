# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    password.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/28 06:58:04 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 12:37:19 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html#constructor-keywords
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# min_verify_time
# deprecated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
    min_verify_time='1s'
)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)