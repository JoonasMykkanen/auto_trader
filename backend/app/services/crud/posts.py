# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    posts.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 14:19:51 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/30 20:37:18 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.models import User
from ...core.models import Post

from sqlalchemy import select
from sqlalchemy import desc

from typing import List



def create_post(db: db_dependency, new_post: Post) -> Post:
    try:
        db.add(new_post)
        db.commit()
    except:
        db.rollback()
        raise


def delete_post(db: db_dependency, to_scrap: Post) -> bool:
    try:
        db.delete(to_scrap)
        db.commit()
    except:
        db.rollback()
        raise


def read_all_posts_by_user(db: db_dependency, target_id: int) -> List[Post]:
    """ Returns all posts made by given user """
    statement = select(Post).filter_by(user_id=target_id)
    posts = db.scalars(statement).all()
    return posts


def read_10_latest_posts_since(db: db_dependency) -> List[Post]:
    """ Return 10 most recent posts from newest to oldest """
    statement = select(Post).order_by(desc(Post.date))
    posts = db.scalars(statement).limit(10).all()
    return posts


def read_10_most_popular_posts(db: db_dependency) -> List[Post]:
    """ Return 10 most upvoted posts since start of current month in descending order"""
    # statement = select(Post).order_by(desc(Post.))
    # TODO: Will need access to other table but dont want to access other tables in this file...