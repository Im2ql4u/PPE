import pytest

from ppe import pieces


@pytest.fixture(scope="session")
def moonlight():
    if "moonlight" not in pieces.available():
        pytest.skip("Moonlight sources not fetched (python -m ppe fetch)")
    return pieces.build_piece("moonlight")


@pytest.fixture(scope="session")
def bach():
    if "bach-prelude-c" not in pieces.available():
        pytest.skip("BWV 846 sources not fetched (python -m ppe fetch)")
    return pieces.build_piece("bach-prelude-c")
