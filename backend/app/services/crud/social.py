# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    social.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/30 14:19:51 by jmykkane          #+#    #+#              #
#    Updated: 2024/05/03 08:32:30 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: /popular && /latest might have performance issues at bigger scales, will need to test with bigger data sets, up to a million or so

from ...core.database import db_dependency
from ...core.schema import CommentContent
from ...core.schema import ReplyContent
from ...core.schema import VoteContent
from ...core.models import Comment
from ...core.models import Reply
from ...core.models import Post
from ...core.models import Vote


from sqlalchemy.orm import aliased
from sqlalchemy import FromClause
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import asc

from typing import List

subquery = select(Vote.post_id, func.sum(Vote.vote_type).label('vote_sum')).group_by(Vote.post_id).alias('vote_sums')
VoteSums = aliased(subquery)



############################################################################
#                                                                          #
#                                VOTES                                     #
#                                                                          #
############################################################################
def create_vote(db: db_dependency, new_vote: Vote) -> Vote:
    try:
        db.add(new_vote)
        db.commit()
        return new_vote
    except:
        db.rollback()
        raise


def delete_vote(db: db_dependency, to_scrap: Vote) -> Vote:
    try:
        db.delete(to_scrap)
        db.commit()
    except:
        db.rollback()
        raise


def read_vote(db: db_dependency, to_find: VoteContent):
    statement = select(Vote).filter_by(user_id=to_find.user_id, post_id=to_find.post_id)
    result = db.scalars(statement).first()
    return result





############################################################################
#                                                                          #
#                             COMMENTS                                     #
#                                                                          #
############################################################################
def create_comment(db: db_dependency, new_comment: Comment) -> Comment:
    try:
        db.add(new_comment)
        db.commit()
        return new_comment
    except:
        db.rollback()
        raise


def delete_comment(db: db_dependency, to_scrap: Comment) -> bool:
    try:
        db.delete(to_scrap)
        db.commit()
        return True
    except:
        db.rollback()
        raise


def read_comment(db: db_dependency, to_find: CommentContent) -> Comment:
    statement = select(Comment).filter_by(user_id=to_find.user_id, post_id=to_find.post_id)
    result = db.scalars(statement).first()
    return result


def read_all_post_comments(db: db_dependency, post_id: int) -> List[Comment]:
    statement = select(Comment).filter_by(post_id=post_id).order_by(asc(Comment.date))
    result = db.scalars(statement).all()
    return result





############################################################################
#                                                                          #
#                              REPLIES                                     #
#                                                                          #
############################################################################
def create_reply(db: db_dependency, new_reply: Reply) -> Reply:
    try:
        db.add(new_reply)
        db.commit()
        return new_reply
    except:
        db.rollback()
        raise


def delete_reply(db: db_dependency, to_scrap: ReplyContent) -> bool:
    try:
        db.delete(to_scrap)
        db.commit()
        return True
    except:
        db.rollback()
        raise


def read_reply(db: db_dependency, to_find: ReplyContent) -> Comment:
    statement = select(Reply).filter_by(user_id=to_find.user_id, comment_id=to_find.comment_id)
    result = db.scalars(statement).first()
    return result


def read_all_comment_replies(db: db_dependency, comment_id: int) -> List[Comment]:
    statement = select(Reply).filter_by(comment_id=comment_id).order_by(asc(Reply.date))
    result = db.scalars(statement).all()
    return result





############################################################################
#                                                                          #
#                                POSTS                                     #
#                                                                          #
############################################################################
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

