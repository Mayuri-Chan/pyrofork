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
from typing import List, Union


class InputReplyToMessage(Object):
    """Contains information about a target replied message.


    Parameters:
        reply_to_message_id (``int``, *optional*):
            ID of the original message you want to reply.

        message_thread_id (``int``, *optional*):
            Unique identifier for the target message thread (topic) of the forum.
            for forum supergroups only.

        reply_to_chat (:obj:`~pyrogram.raw.InputPeer`, *optional*):
            Unique identifier for the origin chat.
            for reply to message from another chat.

        quote_text (``str``, *optional*):
            Text to quote.
            for reply_to_message only.

        quote_entities (List of :obj:`~pyrogram.raw.base.MessageEntity`):
            Entities to quote.
            for reply_to_message only.
    """

    def __init__(
        self, *,
        reply_to_message_id: int = None,
        message_thread_id: int = None,
        reply_to_chat: Union[
            "raw.types.InputPeerChannel",
            "raw.types.InputPeerUser"
        ] = None,
        quote_text: str = None,
        quote_entities: List["raw.base.MessageEntity"] = None
    ):
        super().__init__()

        self.reply_to_message_id = reply_to_message_id
        self.message_thread_id = message_thread_id
        self.reply_to_chat = reply_to_chat
        self.quote_text = quote_text
        self.quote_entities = quote_entities

    def write(self):
        reply_to_msg_id = None
        top_msg_id = None
        if self.reply_to_message_id or self.message_thread_id:
            if self.message_thread_id:
                if not self.reply_to_message_id:
                    reply_to_msg_id = self.message_thread_id
                else:
                    reply_to_msg_id = self.reply_to_message_id
                top_msg_id = self.message_thread_id
            else:
                reply_to_msg_id = self.reply_to_message_id
            return raw.types.InputReplyToMessage(
                reply_to_msg_id=reply_to_msg_id,
                top_msg_id=top_msg_id,
                reply_to_peer_id=self.reply_to_chat,
                quote_text=self.quote_text,
                quote_entities=self.quote_entities
            ).write()
        return None
