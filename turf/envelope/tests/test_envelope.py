import pytest
import os

from turf.envelope import envelope

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["in"])


class TestEnvelope:

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_envelope(self, fixture):

        import ipdb; ipdb.set_trace()

        enveloped = envelope(fixture["in"])

        assert True == True

