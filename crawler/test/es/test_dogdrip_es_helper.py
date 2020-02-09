import sys
import os
import pytest
from datetime import datetime

# append package path into sys.path.
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from es.dogdrip_es_helper import DogdripESHelper  # noqa pylint: disable=import-error


def test_dogdrip_es_helper_connection():
    esh = DogdripESHelper()
    assert esh.connected == True


def test_dogdrip_es_helper_execute_f_comments():
    esh = DogdripESHelper()
    comments = [
        {
            "nickname": "nickname1",
            "content": "content1",
            "like_votes": 10,
            "date": datetime.now()
        },
        {
            "nickname": "nickname2",
            "content": "content2",
            "like_votes": 20,
            "date": datetime.now()
        }
    ]
    esh.index_comments(1, comments)
    esh.delete_comments(1)
