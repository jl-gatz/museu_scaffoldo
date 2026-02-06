from datetime import datetime, timezone
from unittest.mock import patch

import pytest


@pytest.fixture(scope="session")
def frozen_time():
    return datetime(2026, 2, 5, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def mock_time(frozen_time):
    with patch(
        "museu_scaffoldo.modules.visitas.schemas.get_current_time",
        return_value=frozen_time,
    ):
        yield
