# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    error.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/29 17:54:45 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/29 18:32:46 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



class WrongEmailError(Exception):
    pass


class WrongPasswordError(Exception):
    pass
