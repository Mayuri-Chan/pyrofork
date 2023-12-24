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

from pyrogram import raw, types
from ..object import Object


class MediaArea(Object):
    """Content of a media areas in story.

    It should be one of:

    - :obj:`~pyrogram.types.MediaAreaChannelPost`
    """

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates"
    ):
        super().__init__()

        self.coordinates = coordinates

    async def _parse(
        client: "pyrogram.Client",
        media_area: "raw.base.MediaArea"
    ) -> "MediaArea":
        if isinstance(media_area, raw.types.MediaAreaChannelPost):
            return await types.MediaAreaChannelPost._parse(client, media_area)
