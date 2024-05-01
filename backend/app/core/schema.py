# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    schema.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 11:10:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/01 10:09:24 by jmykkane         ###   ########.fr        #
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
    
    # NOTE: Password requirements enforced in frontend
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
