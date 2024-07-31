#  Pyrofork - Telegram MTProto API Client Library for Python
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

from pyrogram import raw
from ..object import Object

class InputStarsTransaction(Object):
    """Content of a stars transaction.

    Parameters:
        id (``str``):
            Unique transaction identifier.

        is_refund (``bool``, *optional*):
            True, If the transaction is a refund.
    """
    def __init__(
        self,
        *,
        id: str,
        is_refund: bool = None
    ):
        super().__init__()

        self.id = id
        self.is_refund = is_refund

    async def write(self):
        return raw.types.InputStarsTransaction(
            id=self.id,
            refund=self.is_refund
        )
