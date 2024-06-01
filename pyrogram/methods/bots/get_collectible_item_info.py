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

import pyrogram
from pyrogram import raw, types


class GetCollectibleItemInfo:
    async def get_collectible_item_info(
        self: "pyrogram.Client",
        username: str = None,
        phone_number: str = None
    ) -> "types.CollectibleInfo":
        """Returns information about a given collectible item that was purchased at https://fragment.com
        .. include:: /_includes/usable-by/users.rst
        You must use exactly one of ``username`` OR ``phone_number``.
        Parameters:
            username (``str``, *optional*):
                Describes a collectible username that can be purchased at https://fragment.com
            phone_number (``str``, *optional*):
                Describes a collectible phone number that can be purchased at https://fragment.com
        Returns:
            :obj:`~pyrogram.types.CollectibleInfo`: On success, a collectible info is returned.
        Example:
            .. code-block:: python
                username = await app.get_collectible_item_info(username="nerd")
                print(username)
        """

        input_collectible = None

        if username:
            input_collectible = raw.types.InputCollectibleUsername(username=username)
        elif phone_number:
            input_collectible = raw.types.InputCollectiblePhone(phone=phone_number)
        else:
            raise ValueError(
                "No argument supplied. Either pass username OR phone_number"
            )

        r = await self.invoke(
            raw.functions.fragment.GetCollectibleInfo(
                collectible=input_collectible
            )
        )

        return types.CollectibleItemInfo._parse(r)
