import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def apptest():
    return AppTest.from_file("app.py").run()


def test_smoketest(apptest):
    assert not apptest.exception, apptest.exception[0].stack_trace
