# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    reply.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/03 07:56:50 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:33:54 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.security import authenticate_token
from ..services.crud.social import create_reply
from ..services.crud.social import delete_reply
from ..services.crud.social import read_reply
from ..core.database import db_dependency
from ..core.schema import ReplyContent
from ..core.models import Reply
from ..core.config import logger

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status

from datetime import timezone
from datetime import datetime
from fastapi import Depends

# TODO: Rate limit
reply_router = APIRouter(
    dependencies=[Depends(authenticate_token)],
    prefix=('/comment')
)


@reply_router.post('/new')
def recieve_vote(db: db_dependency, data: ReplyContent) -> JSONResponse:
    try:
        new_reply = Reply(
            comment_id = data.comment_id,
            user_id = data.user_id,
            content = data.content,
            date = datetime.now(timezone.utc)
        )
        create_reply(new_reply)
        ret = Reply.to_dict()
        JSONResponse(status_code=status.HTTP_201_CREATED, content=ret)

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@reply_router.delete('/remove')
def delete_vote(db: db_dependency, data: ReplyContent) -> bool:
    try:
        to_scrap = read_reply(db, data)
        delete_reply(db, to_scrap)
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )