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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class GetChatGifts:
    async def get_chat_gifts(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited: Optional[bool] = None,
        exclude_upgraded: Optional[bool] = None,
        sort_by_value: Optional[bool] = None,
        limit: int = 0,
        offset: str = ""
    ):
        """Get all gifts owned by specified chat.

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
                
            sort_by_value (``bool``, *optional*):
                Sort star gifts by value.

            offset (``str``, *optional*):
                Offset of the results to be returned.

            limit (``int``, *optional*):
                Maximum amount of star gifts to be returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Gift` objects.

        Example:
            .. code-block:: python

                async for gift in app.get_chat_gifts(chat_id):
                    print(gift)
        """
        peer = await self.resolve_peer(chat_id)

        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.payments.GetSavedStarGifts(
                    peer=peer,
                    offset=offset,
                    limit=limit,
                    exclude_unsaved=exclude_unsaved,
                    exclude_saved=exclude_saved,
                    exclude_unlimited=exclude_unlimited,
                    exclude_limited=exclude_limited,
                    exclude_unique=exclude_upgraded,
                    sort_by_value=sort_by_value
                ),
                sleep_threshold=60
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            user_star_gifts = [
                await types.Gift._parse_saved(self, gift, users, chats)
                for gift in r.gifts
            ]

            if not user_star_gifts:
                return

            for gift in user_star_gifts:
                yield gift

                current += 1

                if current >= total:
                    return

            offset = r.next_offset

            if not offset:
                return
