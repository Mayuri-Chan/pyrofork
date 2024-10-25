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


class ToggleGiftIsSaved:
    async def toggle_gift_is_saved(
        self: "pyrogram.Client",
        sender_user_id: Union[int, str],
        message_id: int,
        is_saved: bool
    ) -> bool:
        """Toggles whether a gift is shown on the current user's profile page.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            sender_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user that sent the gift.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Unique message identifier of the message with the gift in the chat with the user.

            is_saved (``bool``):
                Pass True to display the gift on the user's profile page; pass False to remove it from the profile page.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Hide gift
                app.toggle_gift_is_saved(sender_user_id=user_id, message_id=123, is_saved=False)
        """
        peer = await self.resolve_peer(sender_user_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("sender_user_id must belong to a user.")

        r = await self.invoke(
            raw.functions.payments.SaveStarGift(
                user_id=peer,
                msg_id=message_id,
                unsave=not is_saved
            )
        )

        return r
