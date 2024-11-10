"""Test for base response."""

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
