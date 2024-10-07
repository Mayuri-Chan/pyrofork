#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from random import choice

from pyrogram import raw, types
from ..object import Object


class GiftedPremium(Object):
    """Telegram Premium was gifted to the user

    Parameters:
        gifter_user_id (``int``):
            The identifier of a user that gifted Telegram Premium; 0 if the gift was anonymous

        currency (``str``):
            Currency for the paid amount

        amount (``int``):
            The paid amount, in the smallest units of the currency

        cryptocurrency (``str``):
            Cryptocurrency used to pay for the gift; may be empty if none

        cryptocurrency_amount (``int``):
            The paid amount, in the smallest units of the cryptocurrency; 0 if none

        month_count (``int``):
            Number of months the Telegram Premium subscription will be active
    """

    def __init__(
        self,
        *,
        gifter_user_id: int = None,
        currency: str = None,
        amount: int = None,
        cryptocurrency: str = None,
        cryptocurrency_amount: int = None,
        month_count: int = None
    ):
        super().__init__()

        self.gifter_user_id = gifter_user_id
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.month_count = month_count

    @staticmethod
    async def _parse(
        client,
        gifted_premium: "raw.types.MessageActionGiftPremium",
        gifter_user_id: int
    ) -> "GiftedPremium":
        return GiftedPremium(
            gifter_user_id=gifter_user_id,
            currency=gifted_premium.currency,
            amount=gifted_premium.amount,
            cryptocurrency=getattr(gifted_premium, "crypto_currency", None),
            cryptocurrency_amount=getattr(gifted_premium, "crypto_amount", None),
            month_count=gifted_premium.months
        )
