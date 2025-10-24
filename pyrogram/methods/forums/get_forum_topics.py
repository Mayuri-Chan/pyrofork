#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import logging
from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)

async def get_chunk(
    client: "pyrogram.Client",
    chat_id: Union[int, str],
    offset_date: int,
    offset_id: int,
    offset_topic: int,
    limit: int
):
    peer = await client.resolve_peer(chat_id)

    r = await client.invoke(
        raw.functions.messages.GetForumTopics(
            channel=peer,
            offset_date=offset_date,
            offset_id=offset_id,
            offset_topic=offset_topic,
            limit=limit
        ),
        sleep_threshold=-1
    )

    return r.topics


class GetForumTopics:
    async def get_forum_topics(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0
    ) -> Optional[AsyncGenerator["types.ForumTopic", None]]:
        """Get forum topics from a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            limit (``int``, *optional*):
                Limits the number of topics to be retrieved.
                By default, no limit is applied and all topics are returned.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ForumTopic` objects is returned.

        Example:
            .. code-block:: python

                # get all forum topics
                async for topic in app.get_forum_topics(chat_id):
                    print(topic)

        Raises:
            ValueError: In case of invalid arguments.
        """
        current = 0
        offset_date = 0
        offset_id = 0
        offset_topic = 0
        total = abs(limit) or (1 << 31) - 1
        chunk_limit = min(100, total)

        while True:
            topics = await get_chunk(
                client=self,
                chat_id=chat_id,
                offset_date=offset_date,
                offset_id=offset_id,
                offset_topic=offset_topic,
                limit=chunk_limit
            )

            if not topics:
                return

            last_topic = topics[-1]
            offset_date = int(last_topic.date) if last_topic.date else 0
            offset_id = last_topic.top_message if last_topic.top_message else 0
            offset_topic = last_topic.id

            for topic in topics:
                yield types.ForumTopic._parse(topic)

                current += 1

                if current >= total:
                    return
