# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    posts.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 14:19:51 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 07:17:51 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ...core.database import db_dependency
from ...core.config import logger
from ...core.models import User
from ...core.models import Post
from ...core.models import Vote

from sqlalchemy.orm import aliased

from sqlalchemy import FromClause
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy import func

from typing import Annotated
from fastapi import Depends
from typing import List

subquery = select(Vote.post_id, func.sum(Vote.vote_type).label('vote_sum')).group_by(Vote.post_id).alias('vote_sums')
VoteSums = aliased(subquery)


def create_post(db: db_dependency, new_post: Post) -> Post:
    try:
        db.add(new_post)
        db.commit()
        return new_post
    except:
        db.rollback()
        raise


def delete_post(db: db_dependency, to_scrap: Post) -> bool:
    try:
        db.delete(to_scrap)
        db.commit()
        return True
    except:
        db.rollback()
        raise


def read_post_by_id(db: db_dependency, to_read: int) -> Post:
        statement = select(Post).filter_by(id=to_read)
        result = db.scalars(statement).first()
        return result


def read_all_posts_by_user(db: db_dependency, user_id: int) -> List[Post]:
    """ Returns all posts made by given user """
    statement = select(Post).filter_by(user_id=user_id)
    result = db.scalars(statement).all()
    return result


def read_10_latest_posts(db: db_dependency) -> List[Post]:
    """ Return 10 most recent posts from newest to oldest """
    statement = select(Post).order_by(desc(Post.date)).limit(10)
    result = db.scalars(statement).all()
    latest_posts = { entry.id for entry in result }

    statement = select(VoteSums.c.post_id, VoteSums.c.vote_sum).filter(VoteSums.c.post_id.in_(latest_posts))
    result_2 = db.execute(statement).fetchall()
    vote_counts = { post_id: vote_sum for post_id, vote_sum in result_2 }

    for post in result:
        post.vote_count = vote_counts[post.id]

    return result

def read_10_popular_posts(db: db_dependency) -> List[Post]:
    """ Return 10 most upvoted posts since start of current month in descending order"""
    statement = select(VoteSums.c.post_id, VoteSums.c.vote_sum).order_by(desc(VoteSums.c.vote_sum)).limit(10)
    popular_posts = db.execute(statement).fetchall()

    vote_counts = { post_id: vote_sum for post_id, vote_sum in popular_posts }
    statement = select(Post).filter_by(Post.id.in_(vote_counts.keys()))
    result = db.scalars(statement).all()

    for post in result:
        post.vote_count = vote_counts[post.id]

    return result

