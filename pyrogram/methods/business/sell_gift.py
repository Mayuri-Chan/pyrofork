#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.


from typing import Union

import pyrogram
from pyrogram import raw


class SellGift:
    async def sell_gift(
        self: "pyrogram.Client",
        sender_user_id: Union[int, str],
        message_id: int
    ) -> bool:
        """Sells a gift received by the current user for Telegram Stars.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            sender_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user that sent the gift.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Unique identifier of the message with the gift in the chat with the user.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Convert gift
                app.sell_gift(sender_user_id=user_id, message_id=123)

        """
        peer = await self.resolve_peer(sender_user_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("sender_user_id must belong to a user.")

        r = await self.invoke(
            raw.functions.payments.ConvertStarGift(
                user_id=peer,
                msg_id=message_id
            )
        )

        return r
