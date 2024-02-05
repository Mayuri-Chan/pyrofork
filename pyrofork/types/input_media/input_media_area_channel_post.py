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

from .input_media_area import InputMediaArea

from typing import Union

class InputMediaAreaChannelPost(InputMediaArea):
    """A channel post media area.

    Parameters:
        coordinates (:obj:`~pyrofork.types.MediaAreaCoordinates`):
            Media area coordinates.

        chat_id (``int`` | ``str``):
            Unique identifier (int) or username (str) of the target channel.

        message_id (``int``):
            A single message id.
    """

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates",
        chat_id: Union[int, str],
        message_id: int
    ):
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat_id = chat_id
        self.message_id = message_id

    async def write(self, client: "pyrofork.Client"):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=self.coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id
        )
