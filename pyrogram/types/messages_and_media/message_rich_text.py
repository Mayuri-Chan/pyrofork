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

from typing import Optional, List

import pyrogram
from pyrogram import raw, types
from ..object import Object


class MessageRichText(Object):
    """A Telegram rich text representation."""

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List["types.PageBlock"],
        photos: List["types.Photo"],
        documents: List["types.Document"],
        is_rtl: Optional[bool] = None,
        is_partial: Optional[bool] = None,
    ):
        super().__init__(client)
        self.blocks = blocks
        self.photos = photos
        self.documents = documents
        self.is_rtl = is_rtl
        self.is_partial = is_partial

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        rich_text: "raw.types.RichMessage"
    ) -> Optional["MessageRichText"]:
        
        blocks = [types.PageBlock._parse(client, b) for b in getattr(rich_text, "blocks", None)] if getattr(rich_text, "blocks", None) else []
        photos = [types.Photo._parse(client, p) for p in getattr(rich_text, "photos", None)] if getattr(rich_text, "photos", None) else []
        documents = [types.Document._parse(client, d) for d in getattr(rich_text, "documents", None)] if getattr(rich_text, "documents", None) else []
        return MessageRichText(
            client=client,
            blocks=blocks,
            photos=photos,
            documents=documents,
            is_rtl=getattr(rich_text, "rtl", None),
            is_partial=getattr(rich_text, "part", None)
        )
