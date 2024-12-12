"""OneClick echo response."""

from .base import Response


class ApplePayEchoResponse(Response):
    """ApplePay echo response."""

    def __init__(
        self,
        init_params: str,
        dttm: str,
        result_code: int,
        result_message: str,
    ):
        super().__init__(dttm, result_code, result_message)
        self.init_params = init_params

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "ApplePayEchoResponse":
        """Return payment process result from JSON."""
        return cls(response["initParams"], dttm, result_code, result_message)

    def _get_params_sequence(self) -> tuple:
        return (
            self.init_params,
            self.dttm,
            self.result_code,
            self.result_message,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"init_params='{self.init_params}', "
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}'"
            ")"
        )
