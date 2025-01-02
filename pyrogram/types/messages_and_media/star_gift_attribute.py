#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from datetime import datetime
from typing import Optional, List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import enums
from pyrogram import utils
from ..object import Object


class StarGiftAttribute(Object):
    """Contains information about a star gift attribute.

    Parameters:
        name (``str``):
            Name of the attribute.

        type (:obj:`~pyrogram.enums.StarGiftAttributeType`):
            Type of the attribute.

        rarity (``int``):
            Rarity of the attribute in permilles.
            For example, 15 means 1.5%. So only 1.5% of such collectibles have this attribute.

        sticker (:obj:`~pyrogram.types.Sticker`):
            Information about the sticker.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        name: str,
        type: "enums.StarGiftAttributeType",
        rarity: int,
        sticker: "types.Sticker",
    ):
        super().__init__(client)

        self.name = name
        self.type = type
        self.rarity = rarity
        self.sticker = sticker
        # TODO: Add support for raw.types.StarGiftAttributeOriginalDetails

    @staticmethod
    async def _parse(
        client,
        attr: "raw.base.StarGiftAttribute",
    ) -> "StarGiftAttribute":
        doc = attr.document
        attributes = {type(i): i for i in doc.attributes}

        return StarGiftAttribute(
            name=attr.name,
            type=enums.StarGiftAttributeType(type(attr)),
            sticker=await types.Sticker._parse(client, doc, attributes),
            rarity=attr.rarity_permille,
            client=client
        )
