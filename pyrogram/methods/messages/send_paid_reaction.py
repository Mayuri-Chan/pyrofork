#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import Union

import pyrogram
from pyrogram import raw, types


class SendPaidReaction:
    async def send_paid_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        amount: int,
        anonymous: bool = None
    ) -> "types.MessageReactions":
        """Use this method to send paid reactions on a channel message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            amount (``int``):
                Amount of stars to send.

            anonymous (``bool``, *optional*):
                Pass True to hide yourself from top senders list.

        Returns:
            :obj:`~pyrogram.types.MessageReactions`: On success, MessageReactions is returned.

        Example:
            .. code-block:: python

                # Send a paid reaction
                await app.send_paid_reaction(chat_id, message_id=message_id, amount=5)
        """
        r = await self.invoke(
            raw.functions.messages.SendPaidReaction(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                count=amount,
                random_id=self.rnd_id(),
                private=anonymous
            )
        )
        users = {i.id: i for i in r.users}

        for i in r.updates:
            if isinstance(i, raw.types.UpdateMessageReactions):
                return types.MessageReactions._parse(self, i.reactions, users)
