# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 14:59:59 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 18:29:38 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.auth import get_password_hash
from ..services.crud.users import create_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from ..core.database import db_dependency
from ..core.schema import RegisterSchema
from ..core.schema import LoginSchema
from fastapi import HTTPException
from ..core.config import logger
from ..core.models import User
from fastapi import APIRouter
from fastapi import status
from ..core.error import *
from ..services.auth import authenticate_user

auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.post('/register')
def listen_for_new_users(db: db_dependency, data: RegisterSchema):
    """ Takes in register form and tries to create new user object """
    try:
        password_hash = get_password_hash(data.password)
        new_user = User(
            firstname=data.firstname,
            surname=data.surname,
            birthday=data.birthday,
            email=data.email,
            hash=password_hash
        )
        create_user(db, new_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=f'registering for user {data.email} succesfull')
    
    except IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='email already used')

    except Exception as error:
        db.rollback()
        logger.critical(f'Exception bottom found -> did not catch above: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


# TODO: add token logic to the response
@auth_router.post('/login')
def handle_login(db: db_dependency, data: LoginSchema):
    try:
        user = authenticate_user(db, data.email, data.password)
        return JSONResponse(status_code=200, content='login succesfull')

    except WrongEmailError as error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(error))

    except WrongPasswordError as error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(error))

    except Exception as error:
        logger.critical(f'Exception bottom found -> did not catch above: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')