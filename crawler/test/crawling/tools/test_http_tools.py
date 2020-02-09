import re
import sys
import os
import pytest

# append package path into sys.path.
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from crawling.tools import http_tools  # noqa pylint: disable=import-error


def test_get_html():
    source = http_tools.get_html("https://www.naver.com/")

    # succeed to get html
    assert re.search("https://section.cafe.naver.com/", source) != None

    # wrong url
    with pytest.raises(Exception):
        assert http_tools.get_html("asdfasdfasd")

    # wrong url
    with pytest.raises(Exception):
        assert http_tools.get_html("https://naver.gooogle.co.kr")
    print("succeed to asdf")
