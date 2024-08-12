"""OnceClick payment init request."""

from typing import Optional

from . import payment_init as _pay_init
from .base import BaseRequest


class OneClickPaymentInitRequest(BaseRequest):
    """OneClick payment init request."""

    def __init__(
        # pylint:disable=too-many-locals
        self,
        merchant_id: str,
        private_key: str,
        template_id: str,
        order_no: str,
        return_url: str,
        return_method: _pay_init.ReturnMethod = _pay_init.ReturnMethod.POST,
        payment_method: _pay_init.PaymentMethod = _pay_init.PaymentMethod.CARD,
        client_ip: Optional[str] = None,
        total_amount: Optional[int] = None,
        currency: Optional[_pay_init.Currency] = None,
        close_payment: Optional[bool] = None,
        customer: Optional[_pay_init.CustomerData] = None,
        order: Optional[_pay_init.OrderData] = None,
        client_initiated: bool = True,
        sdk_used: bool = False,
        merchant_data: Optional[bytes] = None,
        ttl_sec: Optional[int] = None,
        language: _pay_init.WebPageLanguage = _pay_init.WebPageLanguage.CS,
    ) -> None:
        super().__init__("oneclick/init", merchant_id, private_key)
        self.template_id = template_id
        self.order_no = order_no
        self.return_url = return_url
        self.return_method = return_method
        self.payment_method = payment_method
        self.client_ip = client_ip
        self.total_amount = total_amount
        self.currency = currency
        self.close_payment = close_payment
        self.customer = customer
        self.order = order
        self.client_initiated = client_initiated
        self.sdk_used = sdk_used
        self.merchant_data = (
            _pay_init.pack_merchant_data(merchant_data)
            if merchant_data
            else None
        )
        self.ttl_sec = ttl_sec
        self.language = language

    def _get_params_sequence(self) -> list:
        return [
            self.merchant_id,
            self.template_id,
            self.order_no,
            self.dttm,
            self.payment_method.value,
            self.client_ip,
            self.total_amount,
            self.currency.value if self.currency else None,
            self.close_payment,
            self.return_url,
            self.return_method.value,
            self.customer.to_sign_text() if self.customer else None,
            self.order.to_sign_text() if self.order else None,
            self.client_initiated,
            self.sdk_used,
            self.merchant_data,
            self.language.value,
            self.ttl_sec,
        ]

    def _as_json(self) -> dict:
        result = {
            "origPayId": self.template_id,
            "orderNo": self.order_no,
            "payMethod": self.payment_method.value,
            "clientIp": self.client_ip,
            "totalAmount": self.total_amount,
            "closePayment": self.close_payment,
            "returnUrl": self.return_url,
            "returnMethod": self.return_method.value,
            "clientInitiated": self.client_initiated,
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
