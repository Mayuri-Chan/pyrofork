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


class ConvertGift:
    async def convert_gift(
        self: "pyrogram.Client",
        message_id: int
    ) -> bool:
        """Convert star gift to stars.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            message_id (``int``):
                Unique message identifier of star gift.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Convert gift
                app.convert_gift(message_id=123)
        """
        r = await self.invoke(
            raw.functions.payments.ConvertStarGift(
                stargift=raw.types.InputSavedStarGiftUser(msg_id=message_id)
            )
        )

        return r
