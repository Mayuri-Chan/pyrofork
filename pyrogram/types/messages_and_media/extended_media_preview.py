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

from pyrogram import raw
from pyrogram import types
from ..object import Object


class ExtendedMediaPreview(Object):
    """A ExtendedMediaPreview.

    Parameters:
        width (``int``, *optional*):
            Media Width.

        height (``int``, *optional*):
            Media Height.

        thumb (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media Thumbnail.

        video_duration (``int``, *optional*):
            Video duration.
    """
    def __init__(
            self,
            *,
            width: int = None,
            height: int = None,
            thumb: "types.Thumbnail" = None,
            video_duration: int = None
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.thumb = thumb
        self.video_duration = video_duration

    @staticmethod
    def _parse(client, media: "raw.types.MessageExtendedMediaPreview") -> "ExtendedMediaPreview":
        thumb = None
        if media.thumb:
            thumb = types.StrippedThumbnail._parse(client, media.thumb)

        return ExtendedMediaPreview(
            width=media.w,
            height=media.h,
            thumb=thumb,
            video_duration=media.video_duration
        )
