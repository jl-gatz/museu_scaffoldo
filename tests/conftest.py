import pytest
from freezegun import freeze_time


@pytest.fixture
def freezer():
    with freeze_time("2026-02-05T12:00:00+00:00") as frozen:
        yield frozen
