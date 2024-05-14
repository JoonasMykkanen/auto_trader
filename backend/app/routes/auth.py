# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 14:59:59 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/14 07:16:40 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.security import get_password_hash
from ..services.security import authenticate_user
from ..services.crud.users import create_user
from ..services.security import get_token
from ..core.database import db_dependency
from ..core.schema import RegisterSchema
from ..core.config import logger
from ..core.schema import Token
from ..core.models import User
from ..core.error import *

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from sqlalchemy.exc import IntegrityError
from typing import Annotated


auth_router = APIRouter(
    prefix='/auth'
)



@auth_router.post('/register')
def listen_for_new_users(db: db_dependency, data: RegisterSchema):
    """ Takes in register form and tries to create new user object """
    try:
        password_hash = get_password_hash(data.password)
        new_user = User(
            firstname = data.firstname,
            surname = data.surname,
            birthday = data.birthday,
            email = data.email,
            hash = password_hash,
            voted = False
        )
        create_user(db, new_user)
        ret = new_user.to_dict()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=ret)
    
    except IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='email already used')

    except Exception as error:
        db.rollback()
        logger.critical(f'Exception bottom found -> did not catch above: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')



@auth_router.post('/login')
def handle_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency) -> JSONResponse:
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        access_token = get_token(form_data.username)
        ret = Token(access_token=access_token, token_type='bearer').dict()
        return JSONResponse(status_code=200, content=ret)

    except WrongEmailError as error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(error))

    except WrongPasswordError as error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(error))

    except Exception as error:
        logger.exception(f'Exception bottom found -> did not catch above: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

