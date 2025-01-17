"""OnceClick payment init request."""
from base64 import b64encode
from typing import Optional

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage

from .base import BaseRequest
from .merchant import pack_merchant_data


class GooglePayInitRequest(BaseRequest):
    """GooglePay payment init request."""

    def __init__(
        # pylint:disable=too-many-locals
        self,
        merchant_id: str,
        private_key: str,
        order_no: str,
        return_url: str,
        return_method: _payment.ReturnMethod = _payment.ReturnMethod.POST,
        client_ip: Optional[str] = None,
        total_amount: Optional[int] = None,
        currency: Optional[_currency.Currency] = None,
        close_payment: Optional[bool] = None,
        payload: Optional[str] = None,
        customer: Optional[_customer.CustomerData] = None,
        order: Optional[_order.OrderData] = None,
        sdk_used: bool = False,
        merchant_data: Optional[bytes] = None,
        ttl_sec: Optional[int] = None,
        language: _webpage.WebPageLanguage = _webpage.WebPageLanguage.CS,
    ) -> None:
        super().__init__("googlepay/init", merchant_id, private_key)
        self.order_no = order_no
        self.return_url = return_url
        self.return_method = return_method
        self.client_ip = client_ip
        self.total_amount = total_amount
        self.currency = currency
        self.close_payment = close_payment
        self.payload = b64encode(payload.encode()).decode()
        self.customer = customer
        self.order = order
        self.sdk_used = sdk_used
        self.merchant_data = (
            pack_merchant_data(merchant_data) if merchant_data else None
        )
        self.ttl_sec = ttl_sec
        self.language = language

    def _get_params_sequence(self) -> list:
        return [
            self.merchant_id,
            self.order_no,
            self.dttm,
            self.client_ip,
            self.total_amount,
            self.currency.value if self.currency else None,
            self.close_payment,
            self.payload,
            self.return_url,
            self.return_method.value,
            self.customer.to_sign_text() if self.customer else None,
            self.order.to_sign_text() if self.order else None,
            self.sdk_used,
            self.merchant_data,
            self.language.value,
            self.ttl_sec,
        ]

    def _as_json(self) -> dict:
        result = {
            "orderNo": self.order_no,
            "clientIp": self.client_ip,
            "totalAmount": self.total_amount,
            "closePayment": self.close_payment,
            "payload": self.payload,
            "returnUrl": self.return_url,
            "returnMethod": self.return_method.value,
            "sdkUsed": self.sdk_used,
            "merchantData": self.merchant_data,
            "language": self.language.value,
            "ttlSec": self.ttl_sec,
        }

        if self.currency:
            result["currency"] = self.currency.value
        if self.customer:
            result["customer"] = self.customer.as_json()
        if self.order:
            result["order"] = self.order.as_json()

        return result
