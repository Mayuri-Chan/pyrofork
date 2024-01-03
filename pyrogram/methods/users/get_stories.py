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
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)

class GetStories:
    async def get_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ) -> Union["types.Story", List["types.Story"]]:
        """Get one or more story from an user by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            story_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single story identifier or an iterable of story ids (as integers) to get the content of the
                story themselves.

        Returns:
            :obj:`~pyrogram.types.Story` | List of :obj:`~pyrogram.types.Story`: In case *story_ids* was not
            a list, a single story is returned, otherwise a list of stories is returned.

        Example:
            .. code-block:: python

                # Get one story
                await app.get_stories(chat_id, 12345)

                # Get more than one story (list of stories)
                await app.get_stories(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]

        rpc = raw.functions.stories.GetStoriesByID(peer=peer, id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            return types.List([await types.Story._parse(self, story, peer) for story in r.stories])
        return await types.Story._parse(self, r.stories[0], peer)
