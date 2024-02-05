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

import pyrofork

from pyrofork import raw, types
from typing import Union
from ..object import Object
from ..update import Update

class StoryDeleted(Object, Update):
    """A deleted story.

    Parameters:
        id (``int``):
            Unique story identifier.

        from_user (:obj:`~pyrofork.types.User`, *optional*):
            Sender of the story.
        
        sender_chat (:obj:`~pyrofork.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.
    """

    def __init__(
        self,
        *,
        client: "pyrofork.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat

    async def _parse(
        client: "pyrofork.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"]
    ) -> "StoryDeleted":
        from_user = None
        sender_chat = None
        if isinstance(peer, raw.types.PeerChannel):
            sender_chat = await client.get_chat(peer.channel_id)
        elif isinstance(peer, raw.types.InputPeerSelf):
            from_user = client.me
        else:
            from_user = await client.get_users(peer.user_id)

        return StoryDeleted(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
            client=client
        )
