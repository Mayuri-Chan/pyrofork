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

from typing import Union

import pyrogram
from pyrogram import raw


class LeaveChat:
    async def leave_chat(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        delete: bool = False
    ):
        """Leave a group chat or channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            delete (``bool``, *optional*):
                Deletes the group chat dialog after leaving (for simple group chats, not supergroups).
                Defaults to False.

        Example:
            .. code-block:: python

                # Leave chat or channel
                await app.leave_chat(chat_id)

                # Leave basic chat and also delete the dialog
                await app.leave_chat(chat_id, delete=True)
        """
        peer = await self.resolve_peer(chat_id)
        if not self.skip_updates:
            await self.storage.remove_state(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return await self.invoke(
                raw.functions.channels.LeaveChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )
        elif isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id,
                    user_id=raw.types.InputUserSelf()
                )
            )

            if delete:
                await self.invoke(
                    raw.functions.messages.DeleteHistory(
                        peer=peer,
                        max_id=0
                    )
                )

            return r
