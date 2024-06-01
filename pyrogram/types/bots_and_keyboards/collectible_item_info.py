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

from datetime import datetime

from pyrogram import raw, utils
from ..object import Object


class CollectibleItemInfo(Object):
    """Contains information about a collectible item and its last purchase.
    Parameters:
        purchase_date (``datetime``):
            Point in time (Unix timestamp) when the item was purchased
        currency (``str``):
            Currency for the paid amount
        amount (``float``):
            The paid amount, in the smallest units of the currency
        cryptocurrency (``str``):
            Cryptocurrency used to pay for the item
        cryptocurrency_amount (``float``):
            The paid amount, in the smallest units of the cryptocurrency
        url (``str``):
            Individual URL for the item on https://fragment.com
            
    """

    def __init__(
        self,
        *,
        purchase_date : datetime,
        currency : str,
        amount: float,
        cryptocurrency: str,
        cryptocurrency_amount: float,
        url: str
    ):
        super().__init__()

        self.purchase_date = purchase_date
        self.currency= currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.url = url

    @staticmethod
    def _parse(
        collectible_info: "raw.types.fragment.CollectibleInfo"
    ) -> "CollectibleItemInfo":
        return CollectibleItemInfo(
            purchase_date=utils.timestamp_to_datetime(collectible_info.purchase_date),
            currency=collectible_info.currency,
            amount=collectible_info.amount,
            cryptocurrency=collectible_info.crypto_currency,
            cryptocurrency_amount=collectible_info.crypto_amount,
            url=collectible_info.url
        )