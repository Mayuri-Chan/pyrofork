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

from ..object import Object


class RequestPeerTypeUser(Object):
    """Object used to request clients to send a user identifier.

    Parameters:
        is_bot (``bool``, *optional*):
            If True, show only Bots.

        is_premium (``bool``, *optional*):
            If True, show only Premium Users.
    """

    def __init__(
        self,
        is_bot: bool=None,
        is_premium: bool=None,
        max: int=1
    ):
        super().__init__()

        self.is_bot = is_bot
        self.is_premium = is_premium
        self.max = max
