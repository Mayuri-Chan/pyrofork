#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class StarGift(Object):
    """A star gift.

    Parameters:
        id (``int``):
            Unique star gift identifier.

        sticker (:obj:`~pyrogram.types.Sticker`):
            Information about the star gift sticker.

        price (``int``):
            Price of this gift in stars.

        convert_price (``int``):
            The number of stars you get if you convert this gift.

        available_amount (``int``, *optional*):
            The number of gifts available for purchase.
            Returned only if is_limited is True.

        total_amount (``int``, *optional*):
            Total amount of gifts.
            Returned only if is_limited is True.

        is_limited (``bool``, *optional*):
            True, if the number of gifts is limited.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        sticker: "types.Sticker",
        price: int,
        convert_price: int,
        available_amount: Optional[int] = None,
        total_amount: Optional[int] = None,
        is_limited: Optional[bool] = None,
    ):
        super().__init__(client)

        self.id = id
        self.sticker = sticker
        self.price = price
        self.convert_price = convert_price
        self.available_amount = available_amount
        self.total_amount = total_amount
        self.is_limited = is_limited

    @staticmethod
    async def _parse(
        client,
        star_gift: "raw.types.StarGift",
    ) -> "StarGift":
        doc = star_gift.sticker
        attributes = {type(i): i for i in doc.attributes}

        return StarGift(
            id=star_gift.id,
            sticker=await types.Sticker._parse(client, doc, attributes),
            price=star_gift.stars,
            convert_price=star_gift.convert_stars,
            available_amount=getattr(star_gift, "availability_remains", None),
            total_amount=getattr(star_gift, "availability_total", None),
            is_limited=getattr(star_gift, "limited", None)
        )
