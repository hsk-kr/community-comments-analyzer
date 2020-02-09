import re
import sys
import os
import pytest

# append package path into sys.path.
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from crawling.community.dogdrip_scraper import DogdripComment, DogdripPost, DogdripScraper  # noqa pylint: disable=import-error


def test_dogdrip_scraper_posts():
    ds = DogdripScraper()
    posts = ds.posts

    # check posts length
    assert len(posts) == 20

    post = posts[0]

    # check a structure of the post
    assert post.num and post.title and post.author and post.vote_num and post.date_str and post.date and post.link


def test_dogdrip_scraper_next_page():
    ds = DogdripScraper()
    ds.next_page()
    posts = ds.posts

    # check posts length
    assert len(posts) == 20


def test_dogdrip_scraper_comments():
    ds = DogdripScraper()
    posts = ds.posts

    # check posts length
    assert len(posts) > 0
    comments = posts[0].comments

    # check comments length
    assert len(comments) > 0

    comment = comments[0]

    # check a structure of the comment
    assert comment.nickname and comment.like_votes >= 0 and comment.date_str and comment.date
