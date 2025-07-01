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

import re
from typing import List, Union

import pyrogram
from pyrogram import raw


class SetPinnedGifts:
    async def set_pinned_gifts(
        self: "pyrogram.Client",
        owner_id: Union[int, str],
        owned_gift_ids: List[str],
    ) -> bool:
        """Change the list of pinned gifts on the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            owner_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            owned_gift_ids (List of ``str``):
                New list of pinned gifts.
                All gifts must be upgraded and saved on the profile page first.
                For a user gift, you can use the message ID (int) of the gift message.
                For a channel gift, you can use the packed format `chatID_savedID` (str).
                For a upgraded gift, you can use the gift link.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Set pinned gifts in user profile
                await app.set_pinned_gifts(received_gift_ids=["123", "456"])
        """
        stargifts = []

        for gift in owned_gift_ids:
            if not isinstance(gift, str):
                raise ValueError(f"gift id has to be str, but {type(gift)} was provided")

            saved_gift_match = re.match(r"^(\d+)_(\d+)$", str(gift))
            slug_match = self.UPGRADED_GIFT_RE.match(str(gift))

            if saved_gift_match:
                stargifts.append(
                    raw.types.InputSavedStarGiftChat(
                        peer=await self.resolve_peer(saved_gift_match.group(1)),
                        saved_id=int(saved_gift_match.group(2))
                    )
                )
            elif slug_match:
                stargifts.append(
                    raw.types.InputSavedStarGiftSlug(
                        slug=slug_match.group(1)
                    )
                )
            else:
                stargifts.append(
                    raw.types.InputSavedStarGiftUser(
                        msg_id=int(gift)
                    )
                )

        r = await self.invoke(
            raw.functions.payments.ToggleStarGiftsPinnedToTop(
                peer=await self.resolve_peer(owner_id),
                stargift=stargifts
            )
        )

        return r
