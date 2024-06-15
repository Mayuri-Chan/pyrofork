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

from typing import Optional

from pyrogram import raw, types
from ..object import Object


class BotApp(Object):
        
    """Contains information about a bot app.
    
        Parameters:
            id (``int``):
                The id of the app.

            short_name (``str``):
                The short name of the app.

            title (``str``):
                The title of the app.

            description (``str``):
                The description of the app.

            photo (``types.Photo``):
                The photo of the app.

            document (:obj:`~pyrogram.types.Document`, *optional*):
                The document of the app.
    """
            
    def __init__(
        self,
        id: int,
        short_name: str,
        title: str,
        description: str,
        photo: "types.Photo",
        document: Optional["types.Document"] = None
    ):
        super().__init__()
        
        self.id = id
        self.short_name = short_name
        self.title = title
        self.description = description
        self.photo = photo
        self.document = document

    @staticmethod
    def _parse(client: "pyrogram.Client", bot_app: "raw.types.BotApp") -> "BotApp":
        document = None
        if isinstance(bot_app.document, raw.types.Document):
            attributes = {type(i): i for i in bot_app.document.attributes}
            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )
            document = types.Document._parse(client, bot_app.document, file_name)
        return BotApp(
            id=bot_app.id,
            short_name=bot_app.short_name,
            title=bot_app.title,
            description=bot_app.description,
            photo=types.Photo._parse(client, bot_app.photo),
            document=document
        )
