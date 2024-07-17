"""Test for base response."""

import pytest

from csobpg.v19.errors import APIMissingParamError
from csobpg.v19.response.base import Response


class _TestResponse(Response):
    """Test response."""

    @classmethod
    def _from_json(
        cls, _: dict, dttm: str, result_code: int, result_message: str
    ) -> "Response":
        """Return response from JSON."""
        return cls(dttm, result_code, result_message)

    def _get_params_sequence(self) -> tuple:
        return tuple()


def test_raise_for_code():
    """Test exception raising for code != 0."""
    resp = _TestResponse("", 100, "message")

    with pytest.raises(APIMissingParamError):
        resp.raise_for_result_code()
