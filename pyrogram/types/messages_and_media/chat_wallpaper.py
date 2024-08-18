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

from ..object import Object
from pyrogram import raw, types

class ChatWallpaper(Object):
    """A service message about a chat wallpaper.

    parameters:
        wallpaper (:obj:`types.Wallpaper`):
            The chat wallpaper.

        is_same (``bool``, *optional*):
            True, if the chat wallpaper is the same as the previous one.

        is_both (``bool``, *optional*):
            True, if the chat wallpaper is for both side.
    """

    def __init__(
        self,
        wallpaper: "types.Wallpaper",
        is_same: bool = None,
        is_both: bool = None
    ):
        super().__init__()
        self.wallpaper = wallpaper
        self.is_same = is_same
        self.is_both = is_both

    @staticmethod
    def _parse(client: "pyrogram.Client", chat_wallpaper: "raw.types.ChatWallpaper") -> "ChatWallpaper":
        return ChatWallpaper(
            wallpaper=types.Wallpaper._parse(client, chat_wallpaper.wallpaper),
            is_same=getattr(chat_wallpaper, "is_same", None),
            is_both=getattr(chat_wallpaper, "is_both", None)
        )
