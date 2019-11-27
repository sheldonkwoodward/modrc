import pytest

from modrc.lib import setup


@pytest.fixture
def initial_setup():
    yield setup.initial_setup()


@pytest.fixture
def teardown():
    yield
    setup.teardown(ignore_errors=True)


@pytest.fixture
def setup_teardown():
    yield setup.initial_setup()
    setup.teardown(ignore_errors=True)
