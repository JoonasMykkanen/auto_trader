# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/16 09:32:22 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/26 15:53:34 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI


# Development router
# TODO: Remove at some point
from .routes.dev import test_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router, prefix='/test')