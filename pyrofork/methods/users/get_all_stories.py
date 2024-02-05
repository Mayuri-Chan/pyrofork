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
from typing import AsyncGenerator, Optional

import pyrofork
from pyrofork import raw
from pyrofork import types

log = logging.getLogger(__name__)

class GetAllStories:
    async def get_all_stories(
        self: "pyrofork.Client"
    ) -> Optional[AsyncGenerator["types.Story", None]]:
        """Get all active stories.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrofork.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all active story
                async for story in app.get_all_stories():
                    print(story)

        Raises:
            ValueError: In case of invalid arguments.
        """

        rpc = raw.functions.stories.GetAllStories()

        r = await self.invoke(rpc, sleep_threshold=-1)

        for peer_story in r.peer_stories:
            for story in peer_story.stories:
                yield await types.Story._parse(self, story, peer_story.peer)
