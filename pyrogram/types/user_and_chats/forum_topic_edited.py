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

from pyrogram import raw
from ..object import Object


class ForumTopicEdited(Object):
    """A service message about a forum topic renamed in the chat.


    Parameters:
        title (``str``):
            Name of the topic.

        icon_color (``int``):
            Color of the topic icon in decimal format.

        custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon.
            
        is_closed (``bool``, *optional*):
            True, if the topic is closed.

        is_hidden (``bool``, *optional*):
            True, if the topic is hidden.
            Valid only for the "General" topic with id=1
    """

    def __init__(
        self, *,
        title: str = None,
        icon_color: int = None,
        custom_emoji_id: int = None,
        is_closed: bool = None,
        is_hidden: bool = None
    ):
        super().__init__()

        self.title = title
        self.icon_color = icon_color
        self.custom_emoji_id = custom_emoji_id
        self.is_closed = is_closed
        self.is_hidden = is_hidden

    @staticmethod
    def _parse(action: "raw.types.MessageActionTopicEdit") -> "ForumTopicEdited":


        return ForumTopicEdited(
            title=getattr(action,"title", None),
            icon_color=getattr(action,"icon_color", None),
custom_emoji_id=getattr(action, "icon_emoji_id", None),
            is_closed=getattr(action, "closed", None),
            is_hidden=getattr(action, "hidden", None)
        )
