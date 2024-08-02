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

import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)

class GetScheduledMessages:
    async def get_scheduled_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]]
    ) -> Union["types.Message", List["types.Message"]]:
        """Get one or more scheduled messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_ids (``int`` | Iterable of ``int``):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of the
                message themselves.

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Get one scheduled message
                await app.get_scheduled_message(chat_id, 12345)

                # Get more than one scheduled message (list of messages)
                await app.get_scheduled_message(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """

        if message_ids is None:
            raise ValueError("No argument supplied. Pass message_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(message_ids, int)
        ids = list(message_ids) if is_iterable else [message_ids]

        rpc = raw.functions.messages.GetScheduledMessages(peer=peer, id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        messages = await utils.parse_messages(self, r)

        return messages if is_iterable else messages[0] if messages else None
