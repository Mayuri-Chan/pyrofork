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

from typing import Optional, Dict

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from ..object import Object


class MessageEntity(Object):
    """One special entity in a text message.
    
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (:obj:`~pyrogram.enums.MessageEntityType`):
            Type of the entity.

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.TEXT_LINK` only, url that will be opened after user taps on the text.

        user (:obj:`~pyrogram.types.User`, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.TEXT_MENTION` only, the mentioned user.

        language (``str``, *optional*):
            For "pre" only, the programming language of the entity text.

        custom_emoji_id (``int``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.CUSTOM_EMOJI` only, unique identifier of the custom emoji.
            Use :meth:`~pyrogram.Client.get_custom_emoji_stickers` to get full information about the sticker.

        collapsed (``bool``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.BLOCKQUOTE` only, whether the blockquote expandable.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "enums.MessageEntityType",
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None,
        language: str = None,
        custom_emoji_id: int = None,
        collapsed: bool = None,
        date: int = None,
        relative: bool = None,
        short_time: bool = None,
        long_time: bool = None,
        short_date: bool = None,
        long_date: bool = None,
        day_of_week: bool = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language
        self.custom_emoji_id = custom_emoji_id
        self.collapsed = collapsed
        self.date = date
        self.relative = relative
        self.short_time = short_time
        self.long_time = long_time
        self.short_date = short_date
        self.long_date = long_date
        self.day_of_week = day_of_week

    @staticmethod
    def _parse(
        client,
        entity: "raw.base.MessageEntity",
        users: Dict[int, "raw.types.User"] = None
    ) -> Optional["MessageEntity"]:
        # Special case for InputMessageEntityMentionName -> MessageEntityType.TEXT_MENTION
        # This happens in case of UpdateShortSentMessage inside send_message() where entities are parsed from the input
        if isinstance(entity, raw.types.InputMessageEntityMentionName):
            entity_type = enums.MessageEntityType.TEXT_MENTION
            user_id = entity.user_id.user_id
        else:
            entity_type = enums.MessageEntityType(entity.__class__)
            user_id = getattr(entity, "user_id", None)

        return MessageEntity(
            type=entity_type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(user_id, None)),
            language=getattr(entity, "language", None),
            custom_emoji_id=getattr(entity, "document_id", None),
            collapsed=getattr(entity, "collapsed", None),
            date=getattr(entity, "date", None),
            relative=getattr(entity, "relative", None),
            short_time=getattr(entity, "short_time", None),
            long_time=getattr(entity, "long_time", None),
            short_date=getattr(entity, "short_date", None),
            long_date=getattr(entity, "long_date", None),
            day_of_week=getattr(entity, "day_of_week", None),
            client=client
        )

    async def write(self):
        args = self.__dict__.copy()

        for arg in ("_client", "type", "user"):
            args.pop(arg)

        if self.user:
            args["user_id"] = await self._client.resolve_peer(self.user.id)

        if not self.url:
            args.pop("url")

        if self.language is None:
            args.pop("language")

        args.pop("custom_emoji_id")
        if self.custom_emoji_id is not None:
            args["document_id"] = self.custom_emoji_id

        if self.type not in [
            enums.MessageEntityType.BLOCKQUOTE,
            enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE
        ]:
            args.pop("collapsed")

        if self.type != enums.MessageEntityType.FORMATTED_DATE:
            for arg in ["date", "relative", "short_time", "long_time", "short_date", "long_date", "day_of_week"]:
                args.pop(arg)

        entity = self.type.value

        if entity is raw.types.MessageEntityMentionName:
            entity = raw.types.InputMessageEntityMentionName

        return entity(**args)
