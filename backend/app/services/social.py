# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    social.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 20:09:40 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:15:28 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: Module contains all the logic for posts, comments, votes and replies

from ..core.schema import PostContent
from ..core.models import Post
from ..core.models import User

def build_new_post_obj(data: PostContent, user: User) -> Post:
    
    return new_post