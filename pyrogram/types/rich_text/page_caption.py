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

from typing import Optional

import pyrogram
from pyrogram import raw, types
from ..object import Object


class PageCaption(Object):
    """Caption of a page block.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`, *optional*):
            Caption text.

        credit (:obj:`~pyrogram.types.RichText`, *optional*):
            Caption credit (author, source, copyright details).
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: Optional["types.RichText"] = None,
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(client)
        self.text = text
        self.credit = credit

    @staticmethod
    def _parse(client: "pyrogram.Client", page_caption: "raw.types.PageCaption") -> Optional["PageCaption"]:
        if not page_caption:
            return None

        if isinstance(page_caption, raw.types.PageCaption):
            return PageCaption(
                client=client,
                text=types.RichText._parse(client, page_caption.text),
                credit=types.RichText._parse(client, page_caption.credit)
            )

        parsed_text = types.RichText._parse(client, page_caption)
        if parsed_text:
            return PageCaption(
                client=client,
                text=parsed_text,
                credit=None
            )

        return None
