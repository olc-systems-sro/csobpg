"""ApplePay payment process request."""

from typing import Optional

from .base import BaseRequest
from ..models.fingerprint import SDK, Browser, Fingerprint

__all__ = [
    "ApplePayProcessRequest",
    "SDK",
    "Browser",
    "Fingerprint",
]


class ApplePayProcessRequest(BaseRequest):
    """ApplePay process request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        fingerprint: Optional[Fingerprint] = None,
    ) -> None:
        super().__init__("applepay/process", merchant_id, private_key)
        self.pay_id = pay_id
        self.fingerprint = fingerprint

    def _get_params_sequence(self) -> list:
        return [
            self.merchant_id,
            self.pay_id,
            self.dttm,
            self.fingerprint.to_sign_text() if self.fingerprint else None,
        ]

    def _as_json(self) -> dict:
        result = {
            "payId": self.pay_id,
        }
        if self.fingerprint:
            result["fingerprint"] = self.fingerprint.as_json()  # type: ignore

        return result
