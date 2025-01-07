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

from typing import Union

import pyrogram
from pyrogram import raw, types


class GetUserGifts:
    async def get_user_gifts(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        offset: str = ""
    ):
        """Get user star gifts.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``str``, *optional*):
                Offset of the results to be returned.

            limit (``int``, *optional*):
                Maximum amount of star gifts to be returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Gift` objects.

        Example:
            .. code-block:: python

                async for gift in app.get_user_gifts(chat_id):
                    print(gift)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("chat_id must belong to a user.")

        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.payments.GetUserStarGifts(
                    user_id=peer,
                    offset=offset,
                    limit=limit
                ),
                sleep_threshold=60
            )

            users = {u.id: u for u in r.users}

            user_star_gifts = [
                await types.Gift._parse_user(self, gift, users)
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
