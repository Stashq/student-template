import pytest

from src.main import add


def test_adding() -> None:
    assert add(2, 2) == 4

    with pytest.raises(AssertionError):
        assert add(2, 3) == 4
