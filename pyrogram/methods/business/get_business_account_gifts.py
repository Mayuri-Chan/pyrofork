#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
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
from pyrogram import raw, types


class GetBusinessAccountGifts:
    async def get_business_account_gifts(
        self: "pyrogram.Client",
        business_connection_id: str,
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited: Optional[bool] = None,
        exclude_upgraded: Optional[bool] = None,
        sort_by_price: Optional[bool] = None,
        limit: int = 0,
        offset: str = "",
    ):
        """Return the gifts received and owned by a managed business account.

        .. note::

            Requires the `can_view_gifts_and_stars` business bot right.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            business_connection_id (``str``):
                Unique identifier of business connection on behalf of which to send the request.

            exclude_unsaved (``bool``, *optional*):
                Pass True to exclude gifts that aren’t saved to the account’s profile page.

            exclude_saved (``bool``, *optional*):
                Pass True to exclude gifts that are saved to the account’s profile page.

            exclude_unlimited (``bool``, *optional*):
                Pass True to exclude gifts that can be purchased an unlimited number of times.

            exclude_limited (``bool``, *optional*):
                Pass True to exclude gifts that can be purchased a limited number of times.

            exclude_upgraded (``bool``, *optional*):
                Pass True to exclude upgraded gifts.

            sort_by_price (``bool``, *optional*):
                Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.

            offset (``str``, *optional*):
                Offset of the first entry to return as received from the previous request.

            limit (``int``, *optional*):
                The maximum number of gifts to be returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Gift` objects.

        Example:
            .. code-block:: python

                async for gift in app.get_business_account_gifts(connection_id):
                    print(gift)
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        connection_info = await self.get_business_connection(business_connection_id)

        while True:
            r = await self.invoke(
                raw.functions.payments.GetSavedStarGifts(
                    peer=await self.resolve_peer(connection_info.user.id),
                    offset=offset,
                    limit=limit,
                    exclude_unsaved=exclude_unsaved,
                    exclude_saved=exclude_saved,
                    exclude_unlimited=exclude_unlimited,
                    exclude_limited=exclude_limited,
                    exclude_unique=exclude_upgraded,
                    sort_by_value=sort_by_price
                ),
                sleep_threshold=60,
                business_connection_id=business_connection_id
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
