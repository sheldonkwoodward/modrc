from click import testing
import pytest


@pytest.fixture
def click_runner():
    runner = testing.CliRunner()
    return runner
