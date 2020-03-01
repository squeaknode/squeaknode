import pytest

from squeaknode.common.greeting import greet


def test_greet():
    response = greet()
    assert 'hello' == response
