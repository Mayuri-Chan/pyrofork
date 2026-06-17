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
from pyrogram import raw, types
from ..object import Object


class OrderedItems(Object):
    """An item in an ordered list containing text or blocks.

    Parameters:
        blocks (List of :obj:`~pyrogram.types.PageBlock`, *optional*):
            A list of page blocks representing the item contents.

        text (:obj:`~pyrogram.types.RichText`, *optional*):
            Rich text representing the item contents.

        num (``str``, *optional*):
            The custom index/number label for the list item.

        value (``int``, *optional*):
            Integer index value.

        item_type (``str``, *optional*):
            The list style type.

        is_checkbox (``bool``, *optional*):
            Whether the list item has a checkbox.

        is_checked (``bool``, *optional*):
            Whether the checkbox is checked.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: Optional[List["types.PageBlock"]] = None,
        text: Optional["types.RichText"] = None,
        num: Optional[str] = None,
        value: Optional[int] = None,
        item_type: Optional[str] = None,
        is_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None
    ):
        super().__init__(client)
        self.blocks = blocks
        self.text = text
        self.num = num
        self.value = value
        self.item_type = item_type
        self.is_checkbox = is_checkbox
        self.is_checked = is_checked

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        item: Union["raw.base.PageListItem", "raw.base.PageListOrderedItem"]
    ) -> Optional["OrderedItems"]:
        if not item:
            return None

        return OrderedItems(
            client=client,
            blocks=[types.PageBlock._parse(client, b) for b in getattr(item, "blocks", [])] if getattr(item, "blocks", None) else None,
            text=types.RichText._parse(client, getattr(item, "text", None)) if getattr(item, "text", None) else None,
            num=getattr(item, "num", None),
            value=getattr(item, "value", None),
            item_type=getattr(item, "type", None),
            is_checkbox=getattr(item, "checkbox", None),
            is_checked=getattr(item, "checked", None)
        )
