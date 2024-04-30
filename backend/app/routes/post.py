# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    post.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 14:20:06 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/30 20:43:41 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from ..services.social import build_new_post_obj
from ..services.auth import authenticate_token
from ..services.crud.posts import create_post

from ..core.database import db_dependency
from ..core.schema import PostContent
from ..core.config import logger
from ..core.models import User
from ..core.models import Post

from typing import Annotated



post_router = APIRouter(
    prefix='/post'
)


@post_router.get('/')
# def listen_root(db: db_dependency, user: Annotated[User, Depends(authenticate_token)]):
def listen_root(user, db):
    # logger.info(user)
    # logger.info(db)
    return "ok"


@post_router.post('/new')
def create_new_post(
    user: Annotated[User, Depends(authenticate_token)],
    db: db_dependency,
    data: PostContent
) -> JSONResponse:
    try:
        new_post = build_new_post_obj(data, user)
        create_post(db, new_post)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='post created succesfully')

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )
    
# TODO: delete post
# TODO: update post
# TODO: get post

# TODO: add likes
# TODO: remove likes
# TODO: add dislikes
# TODO: remove dislikes
