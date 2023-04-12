#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import os
import re
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types

class AddStickerToSet:
    async def add_sticker_to_set(
        self: "pyrogram.Client",
        set_short_name: str,
        sticker: str,
        emoji: str = "🤔",
    ) -> "types.StickerSet":
        """Add a sticker to stickerset.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers.

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

        Returns:
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.add_sticker_to_set("mypack1", "AsJiasp")
        """
        file = None

        if isinstance(sticker, str):
            if os.path.isfile(sticker) or re.match("^https?://", sticker):
                raise ValueError(f"file_id is invalid!")
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference
                )
        else:
            raise ValueError(f"file_id is invalid!")

        r = await self.invoke(
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                sticker=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ]
            )
        )

        return types.StickerSet._parse(r.set)
