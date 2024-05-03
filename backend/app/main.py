# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/16 09:32:22 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:34:32 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from starlette.middleware.cors import CORSMiddleware
from .core.database import engine
from .core.models import Base
from fastapi import FastAPI

from .routes.comment import comment_router
from .routes.reply import reply_router
from .routes.vote import vote_router
from .routes.post import post_router
from .routes.auth import auth_router

# Development router
# TODO: Remove at some point
from .routes.dev import test_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(test_router)

app.include_router(auth_router)
app.include_router(vote_router)
app.include_router(post_router)
app.include_router(reply_router)
app.include_router(comment_router)
