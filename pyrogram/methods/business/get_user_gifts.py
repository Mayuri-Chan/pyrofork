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

from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw, types


class GetUserGifts:
    async def get_user_gifts(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        offset: str = "",
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.UserGift", None]]:
        """Get gifts saved to profile by the given user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``str``, *optional*):
                Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results.

            limit (``int``, *optional*):
                The maximum number of gifts to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by Telegram Server and can be smaller than the specified limit.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.UserGift` objects.

        Example:
            .. code-block:: python

                async for user_gift in app.get_user_gifts(user_id):
                    print(user_gift)
        """
        peer = await self.resolve_peer(user_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("user_id must belong to a user.")

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
                sleep_threshold=max(60, self.sleep_threshold)
            )

            users = {u.id: u for u in r.users}

            user_gifts = [
                await types.UserGift._parse(self, gift, users)
                for gift in r.gifts
            ]

            if not user_gifts:
                return

            for user_gift in user_gifts:
                yield user_gift

                current += 1

                if current >= total:
                    return

            offset = r.next_offset

            if not offset:
                return
