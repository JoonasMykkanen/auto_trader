# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    register.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 14:59:59 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 07:32:14 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import APIRouter


register_router = APIRouter(
    prefix='/register'
)

