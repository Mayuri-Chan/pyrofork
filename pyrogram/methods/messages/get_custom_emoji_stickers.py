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

from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetCustomEmojiStickers:
    async def get_custom_emoji_stickers(
        self: "pyrogram.Client",
        custom_emoji_ids: Union[int, List[int]],
    ) -> Union["types.Sticker", List["types.Sticker"]]:
        """Get information about custom emoji stickers by their identifiers.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            custom_emoji_ids (:obj:`int` | :obj:`List[int]`):
                Custom emoji ID.
                At most 200 custom emoji identifiers can be specified.

        Returns:
            :obj: `~pyrogram.types.Sticker` | List of :obj:`~pyrogram.types.Sticker`: In case *custom_emoji_ids* was not
             a list, a single sticker is returned, otherwise a list of stickers is returned.
        """
        is_list = isinstance(custom_emoji_ids, list)
        custom_emoji_ids = [custom_emoji_ids] if not is_list else custom_emoji_ids

        result = await self.invoke(
            raw.functions.messages.GetCustomEmojiDocuments(
                document_id=custom_emoji_ids
            )
        )

        stickers = pyrogram.types.List()
        for item in result:
            attributes = {type(i): i for i in item.attributes}
            sticker = await types.Sticker._parse(self, item, attributes)
            stickers.append(sticker)

        return stickers if is_list else stickers[0]
