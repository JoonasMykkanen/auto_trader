# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    comment.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/03 07:56:50 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:21:26 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.security import authenticate_token
from ..core.database import db_dependency
from ..core.schema import CommentContent
from ..core.models import Comment
from ..core.config import logger

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status

from datetime import timezone
from datetime import datetime
from fastapi import Depends

# TODO: Rate limit
comment_router = APIRouter(
    dependencies=[Depends(authenticate_token)],
    prefix=('/comment')
)


@comment_router.post('/new')
def recieve_vote(db: db_dependency, data: CommentContent) -> JSONResponse:
    try:
        new_comment = Comment(
            post_id = data.post_id,
            user_id = data.user_id,
            content = data.content,
            date = datetime.now(timezone.utc)
        )
        ret = new_comment.to_dict()
        JSONResponse(status_code=status.HTTP_201_CREATED, content=ret)

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@comment_router.delete('/remove')
def delete_vote(db: db_dependency, data: CommentContent) -> bool:
    try:
        pass

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )