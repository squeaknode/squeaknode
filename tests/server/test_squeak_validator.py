import pytest

from squeakserver.server.squeak_validator import SqueakValidator



def test_validate(validator, example_squeak):
    assert validator.validate(example_squeak)


def test_validate_bad_squeak(validator, bad_squeak):
    assert not validator.validate(bad_squeak)
