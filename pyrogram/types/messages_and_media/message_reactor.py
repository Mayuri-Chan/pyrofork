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
from pyrogram import raw, types
from ..object import Object


class MessageReactor(Object):
    """Contains information about a message reactor.

    Parameters:
        amount (``int``):
            Stars amount.

        is_top (``bool``, *optional*):
            True, if reactor is top.

        is_my (``bool``, *optional*):
            True, if the reaction is mine.

        is_anonymous (``bool``, *optional*):
            True, if reactor is anonymous.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Information about the reactor.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Information about the sender chat.
    """
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        amount: int,
        is_top: bool = None,
        is_my: bool = None,
        is_anonymous: bool = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None
    ):
        super().__init__(client)

        self.amount = amount
        self.is_top = is_top
        self.is_my = is_my
        self.is_anonymous = is_anonymous
        self.from_user = from_user
        self.sender_chat = sender_chat

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        message_reactor: Optional["raw.base.MessageReactor"] = None,
        users: Dict[int, "raw.types.User"] = None,
        chats: Dict[int, "raw.types.Chat"] = None
    ) -> Optional["MessageReactor"]:
        if not message_reactor:
            return None

        is_anonymous = message_reactor.anonymous
        from_user = None
        sender_chat = None
        if not is_anonymous:
            if isinstance(message_reactor.peer_id, raw.types.PeerUser):
                from_user = types.User._parse(
                    client,
                    users.get(message_reactor.peer_id.user_id)
                )
            elif isinstance(message_reactor.peer_id, raw.types.PeerChannel):
                sender_chat = types.Chat._parse_channel_chat(
                    client,
                    chats.get(message_reactor.peer_id.channel_id)
                )

        return MessageReactor(
            client=client,
            amount=message_reactor.count,
            is_top=message_reactor.top,
            is_my=message_reactor.my,
            is_anonymous=is_anonymous,
            from_user=from_user,
            sender_chat=sender_chat
        )
