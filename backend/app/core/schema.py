# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    schema.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 11:10:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:02:35 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pydantic import BaseModel
from pydantic import Field
from datetime import date



class RegisterSchema(BaseModel):
    firstname: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    email: str = Field(min_length=1)
    birthday: date
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class PostContent(BaseModel):
    title: str
    content: str
    author: str
    date: date


class VoteContent(BaseModel):
    user_id: int
    post_id: int
    type: bool


class CommentContent(BaseModel):
    user_id: int
    post_id: int
    content: str
    date: date
