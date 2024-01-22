#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from pyrogram import enums, raw
from ..object import Object

class ReactionType(Object):
    """Contains information about a reaction.

    Parameters:
        type (``enums.ReactionType``, *optional*):
            Reaction type.

        emoji (``str``, *optional*):
            Reaction emoji.

        custom_emoji_id (``int``, *optional*):
            Custom emoji id.
    """
    def __init__(
        self,
        *,
        type: str = "enums.ReactionType",
        emoji: str = None,
        custom_emoji_id: str = None
    ):
        super().__init__()
        self.type = type
        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id

    @staticmethod
    def _parse(
        update: "raw.types.Reaction",
    ) -> Optional["ReactionType"]:
        if isinstance(update, raw.types.ReactionEmpty):
            return None
        elif isinstance(update, raw.types.ReactionEmoji):
            return ReactionType(
                type=enums.ReactionType.EMOJI,
                emoji=update.emoticon
            )
        elif isinstance(update, raw.types.ReactionCustomEmoji):
            return ReactionType(
                type=enums.ReactionType.CUSTOM_EMOJI,
                custom_emoji_id=update.document_id
            )

    def write(self):
        if self.type == enums.ReactionType.EMOJI:
            return raw.types.ReactionEmoji(
                emoticon=self.emoji
            )
        if self.type == enums.ReactionType.CUSTOM_EMOJI:
            return raw.types.ReactionCustomEmoji(
                document_id=self.custom_emoji_id
            )
