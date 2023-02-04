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

import pyrogram
from pyrogram import raw, types
from ..object import Object


class RequestPeerTypeUser(Object):
    """Object used to tell clients to request a suitable user.

    The identifier of the selected user will be shared with the bot when the corresponding button is pressed.

    Parameters:
        is_bot (``bool``, *optional*):
            Pass True to request a bot, pass False to request a regular user.
            If not specified, no additional restrictions are applied.

        is_premium (``bool``, *optional*):
            Pass True to request a premium user, pass False to request a non-premium user.
            If not specified, no additional restrictions are applied.
    """

    def __init__(
        self,
        is_bot: bool = None,
        is_premium: bool = None
    ):
        super().__init__()

        self.is_bot = is_bot
        self.is_premium = is_premium

    async def write(self, _: "pyrogram.Client"):
        return raw.types.RequestPeerTypeUser(
            bot=self.is_bot or None,
            premium=self.is_premium or None
        )
