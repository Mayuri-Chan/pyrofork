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
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from ..object import Object


class UserStarGift(Object):
    """A user star gift.

    Parameters:
        date (``datetime``):
            Date when the star gift was received.

        star_gift (:obj:`~pyrogram.types.StarGift`, *optional*):
            Information about the star gift.

        is_name_hidden (``bool``, *optional*):
            True, if the sender's name is hidden.

        is_saved (``bool``, *optional*):
            True, if the star gift is saved in profile.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            User who sent the star gift.

        text (``str``, *optional*):
            Text message.

        message_id (``int``, *optional*):
            Unique message identifier.

        convert_price (``int``, *optional*):
            The number of stars you get if you convert this gift.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        date: datetime,
        star_gift: "types.StarGift",
        is_name_hidden: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        from_user: Optional["types.User"] = None,
        text: Optional[str] = None,
        message_id: Optional[int] = None,
        convert_price: Optional[int] = None
    ):
        super().__init__(client)

        self.date = date
        self.star_gift = star_gift
        self.is_name_hidden = is_name_hidden
        self.is_saved = is_saved
        self.from_user = from_user
        self.text = text
        self.message_id = message_id
        self.convert_price = convert_price

    @staticmethod
    async def _parse(
        client,
        user_star_gift: "raw.types.UserStarGift",
        users: dict
    ) -> "UserStarGift":
        # TODO: Add entities support
        return UserStarGift(
            date=utils.timestamp_to_datetime(user_star_gift.date),
            star_gift=await types.StarGift._parse(client, user_star_gift.gift),
            is_name_hidden=getattr(user_star_gift, "name_hidden", None),
            is_saved=not user_star_gift.unsaved if getattr(user_star_gift, "unsaved", None) else None,
            from_user=types.User._parse(client, users.get(user_star_gift.from_id)) if getattr(user_star_gift, "from_id", None) else None,
            text=user_star_gift.message.text if getattr(user_star_gift, "message", None) else None,
            message_id=getattr(user_star_gift, "msg_id", None),
            convert_price=getattr(user_star_gift, "convert_stars", None),
            client=client
        )
