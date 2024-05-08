# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    error.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/29 17:54:45 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/08 18:43:04 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import HTTPException
from fastapi import status



class WrongEmailError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class NoTradeEntryError(Exception):
    pass


InvalidTokenError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)