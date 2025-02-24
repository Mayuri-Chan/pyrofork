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

import logging
from typing import Optional, Union

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class GetChatGiftsCount:
    async def get_chat_gifts_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited: Optional[bool] = None,
        exclude_upgraded: Optional[bool] = None
    ) -> int:
        """Get the total count of owned gifts of specified chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            exclude_unsaved (``bool``, *optional*):
                Exclude unsaved star gifts.
                
            exclude_saved (``bool``, *optional*):
                Exclude saved star gifts.
                
            exclude_unlimited (``bool``, *optional*):
                Exclude unlimited star gifts.
                
            exclude_limited (``bool``, *optional*):
                Exclude limited star gifts.
                
            exclude_upgraded (``bool``, *optional*):
                Exclude upgraded star gifts.

        Returns:
            ``int``: On success, the star gifts count is returned.

        Example:
            .. code-block:: python

                await app.get_chat_gifts_count(chat_id)
        """
        peer = await self.resolve_peer(chat_id)

        r = await self.invoke(
            raw.functions.payments.GetSavedStarGifts(
                peer=peer,
                offset="",
                exclude_unsaved=exclude_unsaved,
                exclude_saved=exclude_saved,
                exclude_unlimited=exclude_unlimited,
                exclude_limited=exclude_limited,
                exclude_unique=exclude_upgraded,
                limit=1
            )
        )

        return r.count
