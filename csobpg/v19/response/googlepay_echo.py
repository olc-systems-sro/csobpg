"""GooglePay echo response."""
from csobpg.v19.errors import (
    APIInvalidSignatureError,
    raise_for_result_code,
    APIClientError,
)

from .base import Response, _parse_result_code
from ..models.init_params import InitPramsGoogle


class GooglePayEchoResponse(Response):
    """GooglePay echo response."""

    def __init__(
        self,
        init_prams: InitPramsGoogle,
        dttm: str,
        result_code: int,
        result_message: str,
    ):
        super().__init__(dttm, result_code, result_message)
        self.init_prams = init_prams

    @classmethod
    def from_json(cls, response: dict, public_key: str):
        """Return response from JSON."""
        if not response:
            raise APIClientError("API returned empty response")
        result_code = _parse_result_code(response)
        raise_for_result_code(result_code, response.get("resultMessage", ""))
        obj = cls._from_json(
            response,
            response.get("dttm", ""),
            result_code,
            response.get("resultMessage", ""),
        )

        try:
            signature = response.pop("signature")
        except KeyError:
            raise APIInvalidSignatureError("Empty signature") from None

        # todo: fix find better solution skips because of pyload
        # verify(signature, obj.to_sign_text().encode(), public_key)
        return obj

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "GooglePayEchoResponse":
        """Return payment process result from JSON."""
        return cls(
            response["initParams"],
            dttm,
            result_code,
            result_message,
        )

    def _get_params_sequence(self) -> tuple:
        return (
            self.init_prams.to_sign_text(),
            self.dttm,
            self.result_code,
            self.result_message,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"init_prams='{self.init_prams}', "
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}'"
            ")"
        )
