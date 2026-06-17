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


class Page(Object):
    """A Telegram Instant View Page.

    Parameters:
        url (``str``):
            The URL of the page.

        blocks (List of :obj:`~pyrogram.types.PageBlock`):
            A list of blocks representing the page contents.

        photos (List of :obj:`~pyrogram.types.Photo`):
            A list of photos associated with the page.

        documents (List of :obj:`~pyrogram.types.Document`):
            A list of documents associated with the page.

        is_part (``bool``, *optional*):
            Whether the page is a part.

        is_rtl (``bool``, *optional*):
            Whether the page is right-to-left.

        is_v2 (``bool``, *optional*):
            Whether the page is version 2.

        views (``int``, *optional*):
            The number of views the page has.
    """

    def __init__(
        self,
        client: "pyrogram.Client",
        url: str,
        blocks: List["types.PageBlock"],
        photos: List["types.Photo"],
        documents: List["types.Document"],
        is_part: Optional[bool] = None,
        is_rtl: Optional[bool] = None,
        is_v2: Optional[bool] = None,
        views: Optional[int] = None
    ):
        super().__init__(client)
        self.url = url
        self.blocks = blocks
        self.photos = photos
        self.documents = documents
        self.is_part = is_part
        self.is_rtl = is_rtl
        self.is_v2 = is_v2
        self.views = views

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        page: "raw.base.Page"
    ) -> Optional["Page"]:
        blocks = [types.PageBlock._parse(client, b) for b in getattr(page, "blocks", None)] if getattr(page, "blocks", None) else []
        photos = [types.Photo._parse(client, p) for p in getattr(page, "photos", None)] if getattr(page, "photos", None) else []
        documents = [types.Document._parse(client, d) for d in getattr(page, "documents", None)] if getattr(page, "documents", None) else []
        return Page(
            client=client,
            url=getattr(page, "url", None),
            blocks=blocks,
            photos=photos,
            documents=documents,
            is_part=getattr(page, "part", None),
            is_rtl=getattr(page, "rtl", None),
            is_v2=getattr(page, "v2", None),
            views=getattr(page, "views", None)
        )
