# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    schema.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/27 11:10:46 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/28 12:49:22 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pydantic import BaseModel


# -------------------- auth models -------------------------
class RegisterModel(BaseModel):
    pass

class LoginModel(BaseModel):
    pass

class AuthModel(BaseModel):
    pass



# -------------------- crud models -------------------------