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
from typing import Union, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.file_id import FileId, FileType


class CreateStickerSet:
    async def create_sticker_set(
        self: "pyrogram.Client",
        title: str,
        short_name: str,
        sticker: str,
        user_id: Union[int, str] = None,
        emoji: str = "🤔",
        masks: bool = None
    ) -> Optional["types.Message"]:
        """Create a new stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            title (``str``):
                Stickerset name, 1-64 chars

            short_name (``str``, *optional*):
                Short name of sticker set, to be used in sticker deep links.
                Can contain only english letters, digits and underscores.
                Must begin with a letter, can't contain consecutive underscores and, if called by a bot, must end in "_by_<bot_username>".
                <bot_username> is case insensitive. 1-64 characters.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers.

            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the Stickerset owner.
                For you yourself you can simply use "me" or "self" (users only).
                required for bots.
                default to "me".

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

            masks (``bool``, *optional*):
                Whether this is a mask stickerset.

        Returns:
            :obj:`~pyrogram.types.StickerSet` | ``None``: On success, the StickerSet is returned.

        Example:
            .. code-block:: python

                await app.create_sticker_set("me", "My First Pack", "myfirstpack", "AAjjHjk")
        """

        if self.me.is_bot and user_id is None:
            raise ValueError("user_id is required for bots")

        if isinstance(sticker, str):
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
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id or "me"),
                title=title,
                short_name=short_name,
                stickers=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ],
                masks=masks
            )
        )

        return types.StickerSet._parse(r.set)
