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

from datetime import datetime
from typing import Dict, List

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from ..update import Update


class MessageReactionCountUpdated(Object, Update):
    """Reactions to a message with anonymous reactions were changed.

    These updates are heavy and their changes may be delayed by a few minutes.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            The chat containing the message the user reacted to

        message_id (``int``):
            Unique identifier of the message inside the chat

        date (:py:obj:`~datetime.datetime`):
            Date of change of the reaction

        reactions (:obj:`~pyrogram.types.Reaction`):
            List of reactions that are present on the message
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        message_id: int,
        date: datetime,
        reactions: List["types.Reaction"]
    ):
        super().__init__(client)

        self.chat = chat
        self.message_id = message_id
        self.date = date
        self.reactions = reactions

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: "raw.types.UpdateBotMessageReactions",
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "MessageReactionCountUpdated":
        chat = None
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)
        if peer_id > 0:
            chat = types.Chat._parse_user_chat(client, users[raw_peer_id])
        else:
            chat = types.Chat._parse_chat_chat(client, chats[raw_peer_id])

        return MessageReactionCountUpdated(
            client=client,
            chat=chat,
            message_id=update.msg_id,
            date=utils.timestamp_to_datetime(update.date),
            reactions=[
                types.Reaction._parse_count(
                    client,
                    rt
                ) for rt in update.reactions
            ]
        )
