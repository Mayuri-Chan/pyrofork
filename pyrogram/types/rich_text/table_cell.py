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


class TableCell(Object):
    """A cell in a table row.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`, *optional*):
            Cell text content.

        is_header (``bool``, *optional*):
            Whether this is a header cell.

        is_align_center (``bool``, *optional*):
            Whether the cell content is center-aligned.

        is_align_right (``bool``, *optional*):
            Whether the cell content is right-aligned.

        is_valign_middle (``bool``, *optional*):
            Whether the cell content is vertically middle-aligned.

        is_valign_bottom (``bool``, *optional*):
            Whether the cell content is vertically bottom-aligned.

        colspan (``int``, *optional*):
            The number of columns this cell spans.

        rowspan (``int``, *optional*):
            The number of rows this cell spans.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: Optional["types.RichText"] = None,
        is_header: Optional[bool] = None,
        is_align_center: Optional[bool] = None,
        is_align_right: Optional[bool] = None,
        is_valign_middle: Optional[bool] = None,
        is_valign_bottom: Optional[bool] = None,
        colspan: Optional[int] = None,
        rowspan: Optional[int] = None,
    ):
        super().__init__(client)
        self.text = text
        self.is_header = is_header
        self.is_align_center = is_align_center
        self.is_align_right = is_align_right
        self.is_valign_middle = is_valign_middle
        self.is_valign_bottom = is_valign_bottom
        self.colspan = colspan
        self.rowspan = rowspan

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        cell: "raw.types.PageTableCell"
    ) -> Optional["TableCell"]:
        return TableCell(
            client=client,
            text=types.RichText._parse(client, getattr(cell, "text", None)) if getattr(cell, "text", None) else None,
            is_header=getattr(cell, "header", None),
            is_align_center=getattr(cell, "align_center", None),
            is_align_right=getattr(cell, "align_right", None),
            is_valign_middle=getattr(cell, "valign_middle", None),
            is_valign_bottom=getattr(cell, "valign_bottom", None),
            colspan=getattr(cell, "colspan", None),
            rowspan=getattr(cell, "rowspan", None),
        )
