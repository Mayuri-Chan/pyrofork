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

from datetime import datetime
from typing import Dict, List

import pyrofork
from pyrofork import raw, types, utils
from ..object import Object
from ..update import Update


class MessageReactionUpdated(Object, Update):
    """This object represents a change of a reaction on a message performed by a user.
    A reaction to a message was changed by a user.
    The update isn't received for reactions set by bots.

    These updates are heavy and their changes may be delayed by a few minutes.

    Parameters:
        id (``int``):
            Unique identifier of the message inside the chat
            
        chat (:obj:`~pyrofork.types.Chat`):
            The chat containing the message the user reacted to

        from_user (:obj:`~pyrofork.types.User`, *optional*):
            The user that changed the reaction, if the user isn't anonymous

        actor_chat (:obj:`~pyrofork.types.Chat`, *optional*):
            The chat on behalf of which the reaction was changed, if the user is anonymous

        date (:py:obj:`~datetime.datetime`):
            Date of change of the reaction

        old_reaction (:obj:`~pyrofork.types.ReactionType`):
            Previous list of reaction types that were set by the user

        new_reaction (:obj:`~pyrofork.types.ReactionType`):
            New list of reaction types that have been set by the user

    """

    def __init__(
        self,
        *,
        client: "pyrofork.Client" = None,
        id: int,
        from_user: "types.User",
        actor_chat: "types.Chat",
        date: datetime,
        chat: "types.Chat",
        old_reaction: List["types.ReactionType"],
        new_reaction: List["types.ReactionType"]
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.actor_chat = actor_chat
        self.date = date
        self.chat = chat
        self.old_reaction = old_reaction
        self.new_reaction = new_reaction

    @staticmethod
    def _parse(
        client: "pyrofork.Client",
        update: "raw.types.UpdateBotMessageReaction",
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "MessageReactionUpdated":
        chat = None
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)
        if peer_id > 0:
            chat = types.Chat._parse_user_chat(client, users[raw_peer_id])
        else:
            chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])

        from_user = None
        actor_chat = None

        raw_actor_peer_id = utils.get_raw_peer_id(update.actor)
        actor_peer_id = utils.get_peer_id(update.actor)

        if actor_peer_id > 0:
            from_user = types.User._parse(client, users[raw_actor_peer_id])
        else:
            actor_chat = types.Chat._parse_channel_chat(client, chats[raw_actor_peer_id])

        return MessageReactionUpdated(
            client=client,
            id=update.msg_id,
            from_user=from_user,
            date=utils.timestamp_to_datetime(update.date),
            chat=chat,
            actor_chat=actor_chat,
            old_reaction=[
                types.ReactionType._parse(
                    rt
                ) for rt in update.old_reactions
            ],
            new_reaction=[
                types.ReactionType._parse(
                    rt
                ) for rt in update.new_reactions
            ]
        )