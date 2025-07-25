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

import pyrogram
from pyrogram import raw


class SetGiftResalePrice:
    async def set_gift_resale_price(
        self: "pyrogram.Client",
        owned_gift_id: str,
        resale_star_count: int
    ) -> bool:
        """Change resale price of a unique gift owned by the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            owned_gift_id (``str``):
                Unique identifier of the target gift.
                For a user gift, you can use the message ID (int) of the gift message.
                For a channel gift, you can use the packed format `chatID_savedID` (str).
                For a upgraded gift, you can use the gift link.

            resale_star_count (``int``):
                The new price for the unique gift. Pass 0 to disallow gift resale.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Change resale price of a unique gift
                await app.set_gift_resale_price(owned_gift_id="123456", resale_star_count=100)
        """
        if not isinstance(owned_gift_id, str):
            raise ValueError(f"owned_gift_id has to be str, but {type(owned_gift_id)} was provided")

        saved_gift_match = re.match(r"^(-\d+)_(\d+)$", owned_gift_id)
        slug_match = self.UPGRADED_GIFT_RE.match(owned_gift_id)

        if saved_gift_match:
            stargift = raw.types.InputSavedStarGiftChat(
                peer=await self.resolve_peer(saved_gift_match.group(1)),
                saved_id=int(saved_gift_match.group(2))
            )
        elif slug_match:
            stargift = raw.types.InputSavedStarGiftSlug(
                slug=slug_match.group(1)
            )
        else:
            stargift = raw.types.InputSavedStarGiftUser(
                msg_id=int(owned_gift_id)
            )

        await self.invoke(
            raw.functions.payments.UpdateStarGiftPrice(
                stargift=stargift,
                resell_stars=resale_star_count
            )
        )

        return True
