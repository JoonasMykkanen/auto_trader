# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    vote.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/03 07:22:50 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:20:55 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..services.security import authenticate_token
from ..services.crud.social import create_vote
from ..services.crud.social import delete_vote
from ..services.crud.social import read_vote
from ..core.database import db_dependency
from ..core.schema import VoteContent
from ..core.config import logger
from ..core.models import Vote

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status


vote_router = APIRouter(
    dependencies=[Depends(authenticate_token)],
    prefix='/vote'
)


@vote_router.post('/new')
def recieve_vote(db: db_dependency, data: VoteContent) -> JSONResponse:
    try:
        new_vote = Vote(
            user_id = data.user_id,
            post_id = data.post_id,
            vote_type = 1 if data.type else -1
        )
        create_vote(new_vote)
        ret = new_vote.to_dict()
        JSONResponse(status_code=status.HTTP_201_CREATED, content=ret)

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


@vote_router.delete('/remove')
def delete_vote(db: db_dependency, data: VoteContent) -> bool:
    try:
        to_scrap = read_vote(db, data)
        delete_vote(db, to_scrap)
        return True

    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )