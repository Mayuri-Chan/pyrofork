#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Optional, Union

import pyrogram
from pyrogram import raw
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class StickerSet(Object):
    """A stickerset.

    Parameters:
        id (``Integer``):
            Identifier for this stickerset.

        title (``String``):
            Title of stickerset.

        short_name (``String``):
            Short name of stickerset, used when sharing stickerset using stickerset deep links.

        count (``Integer``):
            Number of stickers in stickerset.

        masks (``Boolean``):
            Is this a mask stickerset.

        animated (``Boolean``):
            Is this a animated stickerset.

        videos (``Boolean``):
            Is this a videos stickerset.

        emojis (``Boolean``):
            Is this a emojis stickerset.
    """

    def __init__(
        self,
        *,
        id: int,
        title: str,
        short_name: str,
        count: int,
        masks: bool = None,
        animated: bool = None,
        videos: bool = None,
        emojis: bool = None
    ):
        self.id = id
        self.title = title
        self.short_name = short_name
        self.count = count
        self.masks = masks
        self.animated = animated
        self.videos = videos
        self.emojis = emojis

    @staticmethod
    def _parse(stickerset: "raw.types.StickerSet") -> "StickerSet":

        return StickerSet(
            id=getattr(stickerset,"id", None),
            title=getattr(stickerset,"title", None),
            short_name=getattr(stickerset,"short_name", None),
            count=getattr(stickerset,"count", None),
            masks=getattr(stickerset,"masks", None),
            animated=getattr(stickerset,"animated", None),
            videos=getattr(stickerset,"videos", None),
            emojis=getattr(stickerset,"emojis", None)
        )
