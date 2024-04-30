# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Social.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 20:09:40 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/30 20:19:48 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: Module contains all the logic for posts, comments, votes and replies

from ..core.schema import PostContent
from ..core.models import Post
from ..core.models import User

def build_new_post(data: PostContent, user: User) -> Post:
    new_post = Post(
        user_id = user.id,
        title = data.title,
        content = data.content,
        author = str(user.firstname + ' ' + user.surname),
        date = data.date
    )
    return new_post