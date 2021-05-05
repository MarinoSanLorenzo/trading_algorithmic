import pytest
from src.utils import *
from src.constants import params
#
# @pytest.fixture()
# def params():
#     return params

@pytest.fixture
def data() -> dict:
    data = get_data(params, stocks=['bitcoin', 'ethereum'])
    return data



class TestData:
    def test_get_data(self, data):
        assert isinstance(data, dict)
        assert data['bitcoin'].shape==data['ethereum'].shape