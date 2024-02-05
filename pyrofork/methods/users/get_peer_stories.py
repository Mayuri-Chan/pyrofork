#  Pyrofork - Telegram MTProto API Client Library for Python
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
from typing import AsyncGenerator, Union, Optional

import pyrofork
from pyrofork import raw
from pyrofork import types

log = logging.getLogger(__name__)

class GetPeerStories:
    async def get_peer_stories(
        self: "pyrofork.Client",
        chat_id: Union[int, str]
    ) -> Optional[AsyncGenerator["types.Story", None]]:
        """Get all active stories from an user/channel by using user identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrofork.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all active story from spesific user/channel
                async for story in app.get_peer_stories(chat_id):
                    print(story)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)


        rpc = raw.functions.stories.GetPeerStories(peer=peer)

        r = await self.invoke(rpc, sleep_threshold=-1)

        for story in r.stories.stories:
            yield await types.Story._parse(self, story, peer)
