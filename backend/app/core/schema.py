# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    schema.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 11:10:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 17:46:34 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# TODO: create pydantic models for data validation
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from datetime import date



class RegisterSchema(BaseModel):
    firstname: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    email: str = Field(EmailStr)
    birthday: date
    
    # NOTE: Password requirements enforced in frontend
    password: str


class LoginSchema(BaseModel):
    email: str = Field(EmailStr)
    password: str