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

import pyrogram

from pyrogram import raw, types, utils

from .media_area import MediaArea

class MediaAreaChannelPost(MediaArea):
    """A channel post media area.

    Parameters:
        coordinates (:obj:`~pyrogram.types.MediaAreaCoordinates`):
            Media area coordinates.

        chat (:obj:`~pyrogram.types.Chat`):
            Media area width.

        message_id (``int``):
            Media area height.
    """

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates",
        chat: "types.Chat",
        message_id: int
    ):
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat = chat
        self.message_id = message_id

    async def _parse(
        client: "pyrogram.Client",
        media_area: "raw.types.MediaAreaChannelPost"
    ) -> "MediaAreaChannelPost":
        channel_id = utils.get_channel_id(media_area.channel_id)
        chat = types.Chat._parse_chat(
            client,
            (
                await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(channel_id)]
                    )
                )
            ).chats[0]
        )
        return MediaAreaChannelPost(
            coordinates=types.MediaAreaCoordinates._parse(media_area.coordinates),
            chat=chat,
            message_id=media_area.msg_id
        )
