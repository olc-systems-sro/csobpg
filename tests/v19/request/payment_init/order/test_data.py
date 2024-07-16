"""Tests for the data module."""

import pytest

from csobpg.v19.request.payment_init import order


@pytest.mark.parametrize(
    "quantity",
    [
        0,
        -1,
        100,
    ],
)
def test_gift_cards_invalid_quantity(quantity: int):
    """Test invalid quantity arg for the GiftCardsData."""
    with pytest.raises(ValueError):
        order.GiftCardsData(quantity=quantity)
