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

from ..object import Object
from pyrogram import enums, raw, types, utils
from typing import Union

class RequestedChat(Object):
    """Contains information about a requested chat.

    Parameters:
        chat_id (``int``):
            Identifier of the chat.

        chat_type (``enums.ChatType``):
            Type of the chat.

        name (``str``, *optional*):
            Name of the chat.

        username (``str``, *optional*):
            Username of the chat.

        photo (``types.ChatPhoto``, *optional*):
            Chat photo.
    """
    def __init__(
        self,
        chat_id: int,
        chat_type: enums.ChatType,
        name: str = None,
        username: str = None,
        photo: "types.ChatPhoto" = None,
    ):
        super().__init__()

        self.chat_id = chat_id
        self.chat_type = chat_type
        self.name = name
        self.username = username
        self.photo = photo

    @staticmethod
    async def _parse(
        client,
        request: Union[
            "raw.types.RequestedPeerChat",
            "raw.types.RequestedPeerChannel",
            "raw.types.PeerChat",
            "raw.types.PeerChannel"
        ]
    ) -> "RequestedChat":
        if isinstance(request, raw.types.RequestedPeerChannel) or isinstance(request, raw.types.PeerChannel):
            type = enums.ChatType.CHANNEL
        else:
            type = enums.ChatType.GROUP
        photo = None
        if getattr(request,"photo", None):
            photo = types.Photo._parse(client, getattr(request,"photo", None), 0)

        return RequestedChat(
            chat_id=utils.get_channel_id(utils.get_raw_peer_id(request)),
            chat_type=type,
            name=getattr(request, "title", None),
            username=getattr(request, "username", None),
            photo=photo,
        )
