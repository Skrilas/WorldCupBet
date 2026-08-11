import pytest

from models.time import Time

@pytest.fixture
def time_um():
    return Time(
        id=758,
        nome="Time 1"
    )

@pytest.fixture
def time_dois():
    return Time(
            id=759,
            nome="Time 2"
        )