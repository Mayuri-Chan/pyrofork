#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
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

from typing import List, Union

import pyrogram
from pyrogram import enums
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from ..object import Object


class ExportedFolderLink(Object):
    """Describes an exported chat folder link.

    Parameters:
        link (``str``):
            The link itself.

        title (``str``, *optional*):
            Title of the folder.
    """

    def __init__(
        self,
        link: str,
        title: str = None
    ):
        super().__init__(None)

        self.link = link
        self.title = title

    @staticmethod
    def _parse(exported_folder_link: "raw.base.ExportedChatFolderLink") -> "ExportedFolderLink":
        return ExportedFolderLink(
            link=getattr(exported_folder_link, "link", None),
            title=getattr(exported_folder_link, "title", None)
        )
