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

from pyrogram import raw, types
from ..object import Object

class StarsStatus(Object):
    """Contains information about stars status.

    Parameters:
        balance (``int``):
            Current balance of stars.

        history (List of :obj:`~pyrogram.types.StarsTransaction`):
            Stars transactions history.
    """
    def __init__(
        self,
        *,
        balance: int,
        history: list
    ):
        super().__init__()
    
        self.balance = balance
        self.history = history
    
    @staticmethod
    def _parse(
        client,
        stars_status: "raw.types.StarsStatus"
    ) -> "StarsStatus":
        users = {user.id: user for user in stars_status.users}
        return StarsStatus(
            balance=stars_status.balance,
            history=[types.StarsTransaction._parse(client, history, users) for history in stars_status.history]
        )
