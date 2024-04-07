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

from datetime import datetime
from typing import Union, List

import pyrogram
from pyrogram import types, utils, raw


class GetBusinessConnection:
    async def get_business_connection(
        self: "pyrogram.Client",
        business_connection_id: str
    ) -> "types.Message":
        """Use this method to get information about the connection of the bot with a business account.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            business_connection_id (``str``):
                Unique identifier of the business connection

        Returns:
            :obj:`~pyrogram.types.BusinessConnection`: On success, the the connection of the bot with a business account is returned.
        """

        r = await self.invoke(
            raw.functions.account.GetBotBusinessConnection(
                connection_id=business_connection_id
            )
        )
        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateBotBusinessConnect
                )
            ):
                return await types.BotBusinessConnection._parse(
                    client=self,
                    bot_connection=i.connection
                )
