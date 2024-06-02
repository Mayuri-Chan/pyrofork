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
from typing import AsyncGenerator

import pyrogram
from pyrogram import raw, types, utils


class SearchGlobalHashtagMessages:
    async def search_global_hashtag_messages(
        self: "pyrogram.Client",
        hashtag: str = "",
        offset_id: int = 0,
        offset_date: datetime = utils.zero_datetime(),
        limit: int = 0,
    ) -> AsyncGenerator["types.Message", None]:
        """Searches for public channel posts with the given hashtag. For optimal performance, the number of returned messages is chosen by Telegram Server and can be smaller than the specified limit.

        If you want to get the posts count only, see :meth:`~pyrogram.Client.search_public_hashtag_messages_count`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            hashtag (``str``, *optional*):
                Hashtag to search for.

            offset_id (``int``, *optional*):
                Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results.

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                Pass a date as offset to retrieve only older messages starting from that date.

            limit (``int``, *optional*):
                The maximum number of messages to be returned. 
                By default, no limit is applied and all posts are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                # Search for "#pyrogram". Get the first 50 results
                async for message in app.search_public_hashtag_messages("#pyrogram"):
                    print(message.text)
                    
        """
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_peer = raw.types.InputPeerEmpty()

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.channels.SearchPosts(
                        hashtag=hashtag,
                        offset_rate=utils.datetime_to_timestamp(offset_date),
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit
                    ),
                    sleep_threshold=60
                ),
                replies=0
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = utils.datetime_to_timestamp(last.date)
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
