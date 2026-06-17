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

from typing import Optional, List, Union

import pyrogram
from pyrogram import enums, raw, types
from ..object import Object


class PageBlockList(Object):
    """An item in a list containing text or nested page blocks.

    Parameters:
        page_block_list_type (:obj:`~pyrogram.enums.PageBlockListType`):
            The type of list items (either text or blocks).

        items (:obj:`~pyrogram.types.RichText` | List of :obj:`~pyrogram.types.PageBlock`):
            The items content.

        is_checkbox (``bool``, *optional*):
            Whether the list item has a checkbox.

        is_checked (``bool``, *optional*):
            Whether the checkbox is checked.
    """

    def __init__(
        self,
        client: "pyrogram.Client",
        page_block_list_type: "enums.PageBlockListType",
        items: Union["types.RichText", List["types.PageBlock"]],
        is_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None
    ):
        super().__init__(client)

        self.page_block_list_type = page_block_list_type
        self.items = items
        self.is_checkbox = is_checkbox
        self.is_checked = is_checked

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        page_block_list: "raw.base.PageListItem"
    ) -> Optional["PageBlockList"]:
        items = []
        if isinstance(page_block_list, raw.types.PageListItemText):
            page_block_list_type = enums.PageBlockListType.TEXTS
        elif isinstance(page_block_list, raw.types.PageListItemBlocks):
            page_block_list_type = enums.PageBlockListType.BLOCKS
        if getattr(page_block_list, "text", None):
            items = types.RichText._parse(client, getattr(page_block_list, "text", None))
        elif getattr(page_block_list, "blocks", None):
            items = [types.PageBlock._parse(client, b) for b in getattr(page_block_list, "blocks", None)]

        return PageBlockList(
            client=client,
            page_block_list_type=page_block_list_type,
            items=items,
            is_checkbox=getattr(page_block_list, "checkbox", None),
            is_checked=getattr(page_block_list, "checked", None)
        )
