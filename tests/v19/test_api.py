"""Tests for the api."""

import json as jsonlib
from dataclasses import dataclass
from typing import Optional

import pytest
from freezegun import freeze_time
from httprest.http.fake_client import FakeHTTPClient, HTTPResponse

from csobpg.v19.api import APIClient
from csobpg.v19.errors import APIError
from csobpg.v19.key import RAMRSAKey, RSAKey
from csobpg.v19.response import PaymentStatus
from csobpg.v19.response.oneclick_echo import OneClickEchoResponse
from csobpg.v19.response.oneclick_payment_init import (
    OneClickPaymentInitResponse,
)
from csobpg.v19.response.oneclick_payment_process import (
    OneClickPaymentProcessResponse,
)
from csobpg.v19.response.payment_close import PaymentCloseResponse
from csobpg.v19.response.payment_init import PaymentInitResponse
from csobpg.v19.response.payment_process import PaymentProcessResponse
from csobpg.v19.response.payment_refund import PaymentRefundResponse
from csobpg.v19.response.payment_reverse import PaymentReverseResponse
from csobpg.v19.response.payment_status import PaymentStatusResponse
from csobpg.v19.signature import sign

_PRIVATE_KEY = RAMRSAKey("tests/v19/data/merchant.key")
_PUBLIC_KEY = RAMRSAKey("tests/v19/data/merchant.pub")


@dataclass
class _Components:
    api: APIClient
    base_url: str
    http_client: FakeHTTPClient

    @classmethod
    def compose(
        cls,
        merchant_id: str = "mid",
        private_key: RSAKey = _PRIVATE_KEY,
        public_key: RSAKey = _PUBLIC_KEY,
        base_url: str = "https://api.com",
        http_client: Optional[FakeHTTPClient] = None,
    ) -> "_Components":
        """Compose components."""
        http_client = http_client or FakeHTTPClient()
        return cls(
            APIClient(merchant_id, private_key, public_key, base_url, http_client),
            base_url,
            http_client,
        )


@freeze_time("1955-11-12")
def test_init_payment():
    """Test for the payment init."""
    resp = PaymentInitResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.init_payment("oid", 1000, "http://return.com")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "cart": [{"amount": 1000, "name": "Payment", "quantity": 1}],
                "closePayment": True,
                "currency": "CZK",
                "dttm": "19551112000000",
                "language": "cs",
                "merchantId": comps.api.merchant_id,
                "orderNo": "oid",
                "payMethod": "card",
                "payOperation": "payment",
                "returnMethod": "POST",
                "returnUrl": "http://return.com",
                "signature": (
                    "mk2a83Kfc1jM2kUzOX2c4wQljQFg2zgc1n19Oyh3iVXIBRcpWfGS3jHaa"
                    "h6rw3xnXDyA5ye5J2a/y00FLU3bBc4EPvnV3FLADQkJaLhgYsMX22wznm"
                    "CpGcF9MEk165b7wTdxq8hhuTjTTL+FehNYAt2WBoPRlOSSlWGgT4o6j0b"
                    "4iwe9F82vARknJVAlTXDipjQx9JJqkcPYyBXd6Zxnr4N35YrOzEfZ4DyX"
                    "7uiZgFd2QKRPo/VKZvmmiPSom7zeFdipukGvyIdXG/1Wl+iScCBf/Z93V"
                    "Xpzrtp9l4IbfB4hyThjedQ+Bd1/PitlJeTplscfffPExosZHVK7usguAQ"
                    "=="
                ),
                "totalAmount": 1000,
                "ttlSec": 600,
            },
            "cert": None,
            "method": "post",
            "url": f"{comps.base_url}/payment/init",
        },
    ]


@freeze_time("1955-11-12")
def test_get_payment_status():
    """Test for the payment status get."""
    resp = PaymentStatusResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.get_payment_status("oid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": None,
            "method": "get",
            "url": (
                f"{comps.base_url}/payment/status/mid/oid/19551112000000/qOvsS"
                "hm%2FqBiQmwar3tCQoc%2F9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn8R5Nw"
                "bsoZKqLW7pBfDQtgAhiWmVJEywguwwcplwc57bc%2BLCjgeu0mMGUxvJcmt5k"
                "jRXFabzQHc3Pheno2p4jf%2Fp5O7m67JdsSTonrB7J3SvxiX37dIdsXEOtT4Q"
                "Sf2G1cENqUfQBqL6z40eZmJ2SB6nKy8Ji0QwQN07KFHgBdM0Jt50ZJJ0uQk8W"
                "Ef%2BwJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp%2Bmn9Dfck4%2BrjVCB9ZpiE3"
                "%2B11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE%2FagxmRQ%3D%3D"
            ),
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_reverse_payment():
    """Test for the payment reversal."""
    resp = PaymentReverseResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.reverse_payment("oid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "qOvsShm/qBiQmwar3tCQoc/9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn"
                    "8R5NwbsoZKqLW7pBfDQtgAhiWmVJEywguwwcplwc57bc+LCjgeu0mMGUx"
                    "vJcmt5kjRXFabzQHc3Pheno2p4jf/p5O7m67JdsSTonrB7J3SvxiX37dI"
                    "dsXEOtT4QSf2G1cENqUfQBqL6z40eZmJ2SB6nKy8Ji0QwQN07KFHgBdM0"
                    "Jt50ZJJ0uQk8WEf+wJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp+mn9Dfck4+"
                    "rjVCB9ZpiE3+11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE/agxmRQ"
                    "=="
                ),
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/reverse",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_close_payment():
    """Test for the payment close."""
    resp = PaymentCloseResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.close_payment("oid", total_amount=1010)
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "hc6JmmMa9JOOb6lKnHclSQ1OZJWX5sI71oxyAu5FJlQ2+JoiGKOGOMMJH"
                    "Z+VA+nSawjNYcvZg9eDM4c3DYFLYjLI0CDZojXb7tg/jtW9eGBhgNERGR"
                    "JoTPLviWAbztQoLYR09sCi0U/X9Hwn7A14P7yjQIjscphRVWHDo6ye/G4"
                    "3byRURoSyMqdd3DJwRlttJbvmOXVqRk6Qh6gPJRMMXIe0fPmGNO2YykFb"
                    "r4ICeA9uIqIgKRUEGEEIQmMZZTf1BdQv9VNfkBR0+JXzgyp62fjIxuepd"
                    "24VrxunwveNhnTB6ynhIbDOz5yhs0c+wEmkxg5Yp0RNxCKZB+ixr/JZuA"
                    "=="
                ),
                "totalAmount": 1010,
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/close",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_refund_payment():
    """Test for the payment refund."""
    resp = PaymentRefundResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.refund_payment("oid", amount=1010)
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "amount": 1010,
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "hc6JmmMa9JOOb6lKnHclSQ1OZJWX5sI71oxyAu5FJlQ2+JoiGKOGOMMJH"
                    "Z+VA+nSawjNYcvZg9eDM4c3DYFLYjLI0CDZojXb7tg/jtW9eGBhgNERGR"
                    "JoTPLviWAbztQoLYR09sCi0U/X9Hwn7A14P7yjQIjscphRVWHDo6ye/G4"
                    "3byRURoSyMqdd3DJwRlttJbvmOXVqRk6Qh6gPJRMMXIe0fPmGNO2YykFb"
                    "r4ICeA9uIqIgKRUEGEEIQmMZZTf1BdQv9VNfkBR0+JXzgyp62fjIxuepd"
                    "24VrxunwveNhnTB6ynhIbDOz5yhs0c+wEmkxg5Yp0RNxCKZB+ixr/JZuA"
                    "=="
                ),
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/refund",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_api_error():
    """Test for an API error."""
    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    401,
                    jsonlib.dumps({"resultCode": 110}).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    with pytest.raises(APIError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_get_payment_process_url():
    """Test for the payment process URL build."""
    comps = _Components.compose()
    assert comps.api.get_payment_process_url("oid") == (
        f"{comps.base_url}/payment/process/mid/oid/19551112000000/qOvsShm%2FqB"
        "iQmwar3tCQoc%2F9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn8R5NwbsoZKqLW7pBfDQt"
        "gAhiWmVJEywguwwcplwc57bc%2BLCjgeu0mMGUxvJcmt5kjRXFabzQHc3Pheno2p4jf%2"
        "Fp5O7m67JdsSTonrB7J3SvxiX37dIdsXEOtT4QSf2G1cENqUfQBqL6z40eZmJ2SB6nKy8"
        "Ji0QwQN07KFHgBdM0Jt50ZJJ0uQk8WEf%2BwJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp%2B"
        "mn9Dfck4%2BrjVCB9ZpiE3%2B11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE%2Fagx"
        "mRQ%3D%3D"
    )


@freeze_time("1955-11-12")
def test_echo():
    """Test for the echo."""
    comps = _Components.compose(
        http_client=FakeHTTPClient(responses=[HTTPResponse(200, b"", {})])
    )
    comps.api.echo()
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "signature": (
                    "i73Jtef6OPfGlH6I/YbwNv9vEeTUVtlQvJ0ZHOcaoWv2/NfGAhLdjiyWI"
                    "uDys0IJk17ndTCZdbDOF4Ku/sj47uI5qAaJskLeHGZaFytFcIEmd7R9sY"
                    "O4Ath1UvXmNdpNJyQXwlqnQrMDwcxRLWaWclQWZeTjjihxFNWbN5sN0xC"
                    "+BJgY73AuvmiC0yakQE2eWPFcS2ErvTgPb5mb3Wudut8O5JzflTNEGjmv"
                    "T+ln2ndB8qefvm5vcRYvoNeJcF/yXTRUjy4lMf8Ua9lHSwYNz3sjgbn1b"
                    "B7xcJRFUFfp94W8gWBxcflxVmk4/s0Pe7CPJxuTITi1rSGS8sayGGywZA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/echo",
            "cert": None,
        },
    ]


def test_process_gateway_return():
    """Test for the gateway return processing."""
    resp = PaymentProcessResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
        auth_code="acode",
    )
    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "authCode": resp.auth_code,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }
    comps = _Components.compose()

    assert comps.api.process_gateway_return(resp_json).auth_code == "acode"
    assert not comps.http_client.history


@freeze_time("1955-11-12")
def test_oneclick_init_payment():
    """Test for the oneclick payment init."""
    resp = OneClickPaymentInitResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.oneclick_init_payment("tid", "oid", "http://return.com")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "clientInitiated": True,
                "dttm": "19551112000000",
                "language": "cs",
                "merchantId": comps.api.merchant_id,
                "orderNo": "oid",
                "origPayId": "tid",
                "payMethod": "card",
                "returnMethod": "POST",
                "returnUrl": "http://return.com",
                "sdkUsed": False,
                "signature": (
                    "xFSQtXGdRvVtpYwSMD2qa9jhHGog4uO///H1IRFlCLwWTy2ASD6JFzSz8"
                    "ma1hwXL/FKjL/TFqGin0MDG8cuU0AnLineL007Gih6vndA3I+Vw8RwpQg"
                    "uQbqwGWZ4AO6GT8HNrjQlsnV8+zRzhLZ8XXaURnKNxtZUQg2Dgce1WCxY"
                    "xUfZL+mDgpjYlKGiW53lBOhYTdR9mxdko++CMbOPyg+sjfaUuw+Rves+f"
                    "SIdXle2eEKPYS71rBroAZ/ME2jjg1I9IYXbdUXxJ3xP4X7WobQYoob9P9"
                    "pgCbUkAowK0RhxEXYq6CQE8IwZgc/4ps7TjMK2oTz9oyjHIbOEk6C8CSQ"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/oneclick/init",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_oneclick_process():
    """Test for the oneclick process."""
    resp = OneClickPaymentProcessResponse(
        "pid", "20240919164156", 0, "", PaymentStatus.IN_PROGRESS
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,  # type: ignore
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    resp = comps.api.oneclick_process("tid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "tid",
                "signature": (
                    "0OT7wNlDCoaMtbvgmW0wf0OHu8SxRobRzHdyPEen/69prijU9QxfjNYV5"
                    "Sx7ucER8NBQOis9BxolIZgvhSeo+aH0+u6BARzfXY35CgTglnZfGBIYKA"
                    "eIMmv4xd3AaSMboMbh5js0fb1kBNsS+ouQTgzkLCZnubvUHhg1H9A4vSc"
                    "Tf+opG5DB+OJq1UmmRjmaI8Sirx52RH3mcJhjNd+/cd9n4MdbAwRrb9UF"
                    "vocHii6im3QEf8UvOCZcvv/npC6GTkLyazvNmSaol4ZtJ7aYP08jexm5Q"
                    "mTVyfpVko2XgbQ/SuYSGEBZ3iaMD4H6SVkwMjZ6OuqBVir6xC8eV5gCuA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/oneclick/process",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_oneclick_echo():
    """Test for the oneclick echo."""
    resp = OneClickEchoResponse("pid", "20240919164156", 0, "")

    resp_json = {
        "origPayId": resp.template_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ]
        )
    )
    comps.api.oneclick_echo("tid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "origPayId": "tid",
                "signature": (
                    "0OT7wNlDCoaMtbvgmW0wf0OHu8SxRobRzHdyPEen/69prijU9QxfjNYV5"
                    "Sx7ucER8NBQOis9BxolIZgvhSeo+aH0+u6BARzfXY35CgTglnZfGBIYKA"
                    "eIMmv4xd3AaSMboMbh5js0fb1kBNsS+ouQTgzkLCZnubvUHhg1H9A4vSc"
                    "Tf+opG5DB+OJq1UmmRjmaI8Sirx52RH3mcJhjNd+/cd9n4MdbAwRrb9UF"
                    "vocHii6im3QEf8UvOCZcvv/npC6GTkLyazvNmSaol4ZtJ7aYP08jexm5Q"
                    "mTVyfpVko2XgbQ/SuYSGEBZ3iaMD4H6SVkwMjZ6OuqBVir6xC8eV5gCuA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/oneclick/echo",
            "cert": None,
        },
    ]
