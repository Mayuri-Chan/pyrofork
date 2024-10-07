#  Pyrofork - Telegram MTProto API Client Library for Python
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

from pyrogram import raw
from ..object import Object

class LabeledPrice(Object):
    """This object represents a price for goods or services.

    Parameters:
        label (``str``):
            Portion label.

        amount (``int``):
            Price of the product in the smallest units of the currency (integer, not float/double).
            The minimum amuont for telegram stars is 1.
            The minimum amount for other currencies is US$1.
            you need to add 2 extra zeros to the amount (except stars), example 100 for 1 usd.
    """

    def __init__(
        self,
        label: str,
        amount: int
    ):
        self.label = label
        self.amount = amount

    def write(self):
        return raw.types.LabeledPrice(
            label=self.label,
            amount=self.amount
        )
