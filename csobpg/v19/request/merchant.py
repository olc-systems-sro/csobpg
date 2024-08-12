"""Merchant wrappers."""

from base64 import b64encode


def pack_merchant_data(data: bytes) -> str:
    """Pack Merchant Data.

    It must be transferred as BASE64 encoded string.
    """
    encoded = b64encode(data).decode("UTF-8")

    if len(encoded) > 255:
        raise ValueError(
            "Merchant data length encoded to BASE64 is over 255 chars"
        )

    return encoded
