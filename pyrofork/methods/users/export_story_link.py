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
from typing import Union

import pyrofork
from pyrofork import raw
from pyrofork import types

log = logging.getLogger(__name__)

class ExportStoryLink:
    async def export_story_link(
        self: "pyrofork.Client",
        chat_id: Union[int, str],
        story_id: int,
    ) -> types.ExportedStoryLink:
        """Get one story link from an user by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            story_id (``int``):
                Pass a single story identifier of story (as integers).

        Returns:
            :obj:`~pyrofork.types.ExportedStoryLink`: a single story link is returned.

        Example:
            .. code-block:: python

                # Get story link
                await app.export_story_link(chat_id, 12345)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.stories.ExportStoryLink(peer=peer, id=story_id)

        r = await self.invoke(rpc, sleep_threshold=-1)

        return types.ExportedStoryLink._parse(r)
