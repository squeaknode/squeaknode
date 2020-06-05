import pytest

from squeakserver.common.greeting import greet


def test_greet():
    response = greet()
    assert 'hello' == response
