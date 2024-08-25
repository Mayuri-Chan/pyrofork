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

import os
import re

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.file_id import FileId, FileType

from typing import Union

class AddStickerToSet:
    async def add_sticker_to_set(
        self: "pyrogram.Client",
        set_short_name: str,
        sticker: str,
        user_id: Union[int, str] = None,
        emoji: str = "🤔",
    ) -> "types.StickerSet":
        """Add a sticker to stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to add a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a sticker from the Internet,
                pass a file path as string to upload a new sticker that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the Stickerset owner.
                For you yourself you can simply use "me" or "self" (users only).
                required for bots.
                default to "me".

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

        Returns:
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.add_sticker_to_set("mypack1", "AsJiasp")
        """

        if isinstance(sticker, str):
            if self.me.is_bot and user_id is None:
                raise ValueError("user_id is required for bots")
            if os.path.isfile(sticker) or re.match("^https?://", sticker):
                document = await self.send_document(
                    user_id or "me",
                    sticker,
                    force_document=True,
                    disable_notification=True
                )
                uploaded_media = utils.get_input_media_from_file_id(document.document.file_id, FileType.DOCUMENT)
                media = uploaded_media.id
                _ = await document.delete()
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference
                )
        else:
            if self.me.is_bot and user_id is None:
                raise ValueError("user_id is required for bots")
            document = await self.send_document(
                user_id or "me",
                sticker,
                force_document=True,
                disable_notification=True
            )
            uploaded_media = utils.get_input_media_from_file_id(document.document.file_id, FileType.DOCUMENT)
            media = uploaded_media.id
            _ = await document.delete()

        r = await self.invoke(
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                sticker=raw.types.InputStickerSetItem(
                    document=media,
                    emoji=emoji
                )
            )
        )

        return types.StickerSet._parse(r.set)
