# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    post.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 14:20:06 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:17:01 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.exc import IntegrityError

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from ..services.security import authenticate_token
from ..services.crud.social import *

from ..core.database import db_dependency
from ..core.schema import PostContent
from ..core.config import logger
from ..core.models import User
from ..core.models import Post

from datetime import datetime
from datetime import timezone
from typing import Annotated
import time

# TODO: RATE LIMIT
post_router = APIRouter(
    dependencies=[Depends(authenticate_token)],
    prefix='/post'
)


@post_router.post('/new')
def create_new_post(
    user: Annotated[User, Depends(authenticate_token)],
    db: db_dependency,
    data: PostContent
) -> JSONResponse:
    try:
        new_post = Post(
            user_id = user.id,
            title = data.title,
            content = data.content,
            author = data.author,
            date = datetime.now(timezone.utc)
        )
        create_post(db, new_post)
        ret = new_post.to_dict()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=ret
        )
    
    except IntegrityError as error:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=f'post with title: {new_post.title} already exists. Has to be unique.'
        )
    
    except Exception as error:
        db.rollback()
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@post_router.delete('/delete/{post_id}')
def handle_delete_post(db: db_dependency, post_id: int) -> JSONResponse:
    try:
        delete_post(db, post_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f'post id: {post_id} deleted succesfully'
        )

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@post_router.get('/my')
def get_all_my_posts(
    user: Annotated[User, Depends(authenticate_token)],
    db: db_dependency
) -> JSONResponse:
    try:
        posts = read_all_posts_by_user(db, user.id)
        ret = []
        for post in posts:
            ret.append(post.to_dict())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ret
        )
            
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@post_router.get('/latest')
def get_latest(db: db_dependency) -> JSONResponse:
    try:
        posts = read_10_latest_posts(db)
        ret = []
        for post in posts:
            ret.append(post.to_dict())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ret
        )

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@post_router.get('/popular')
def get_popular(db: db_dependency) -> JSONResponse:
    try:
        posts = read_10_popular_posts(db)
        ret = []
        for post in posts:
            dict_repr = post.to_dict()
            dict_repr['vote_count'] = post.vote_count
            ret.append(dict_repr)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ret
        )
    
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )
