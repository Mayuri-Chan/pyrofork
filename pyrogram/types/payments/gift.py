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

from datetime import datetime
from typing import Optional

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class Gift(Object):
    """Describes a gift that can be sent to another user.

    Parameters:
        id (``int``):
            Unique identifier of the gift.

        sticker (:obj:`~pyrogram.types.Sticker`):
            The sticker representing the gift.

        star_count (``int``):
            Number of Telegram Stars that must be paid for the gift.

        default_sell_star_count (``int``):
            Number of Telegram Stars that can be claimed by the receiver instead of the gift by default. If the gift was paid with just bought Telegram Stars, then full value can be claimed.

        remaining_count (``int``, *optional*):
            Number of remaining times the gift can be purchased by all users; None if not limited or the gift was sold out.

        total_count (``int``, *optional*):
            Number of total times the gift can be purchased by all users; None if not limited.

        first_send_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time (Unix timestamp) when the gift was send for the first time; for sold out gifts only.

        last_send_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time (Unix timestamp) when the gift was send for the last time; for sold out gifts only.

        is_limited (``bool``, *optional*):
            True, if the number of gifts is limited.

        is_sold_out (``bool``, *optional*):
            True, if the star gift is sold out.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        sticker: "types.Sticker",
        star_count: int,
        default_sell_star_count: int,
        remaining_count: Optional[int] = None,
        total_count: Optional[int] = None,
        first_send_date: Optional[datetime] = None,
        last_send_date: Optional[datetime] = None,
        is_limited: Optional[bool] = None,
        is_sold_out: Optional[bool] = None,
    ):
        super().__init__(client)

        self.id = id
        self.sticker = sticker
        self.star_count = star_count
        self.default_sell_star_count = default_sell_star_count
        self.remaining_count = remaining_count
        self.total_count = total_count
        self.first_send_date = first_send_date
        self.last_send_date = last_send_date
        self.is_limited = is_limited
        self.is_sold_out = is_sold_out

    @staticmethod
    async def _parse(
        client,
        star_gift: "raw.types.StarGift",
    ) -> "Gift":
        doc = star_gift.sticker
        attributes = {type(i): i for i in doc.attributes}

        return Gift(
            id=star_gift.id,
            sticker=await types.Sticker._parse(client, doc, attributes),
            star_count=star_gift.stars,
            default_sell_star_count=star_gift.convert_stars,
            remaining_count=getattr(star_gift, "availability_remains", None),
            total_count=getattr(star_gift, "availability_total", None),
            first_send_date=utils.timestamp_to_datetime(getattr(star_gift, "first_sale_date", None)),
            last_send_date=utils.timestamp_to_datetime(getattr(star_gift, "last_sale_date", None)),
            is_limited=getattr(star_gift, "limited", None),
            is_sold_out=getattr(star_gift, "sold_out", None),
            client=client
        )
