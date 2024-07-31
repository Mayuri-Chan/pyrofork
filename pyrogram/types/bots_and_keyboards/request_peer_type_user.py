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
        button_id (``int``, *optional*):
            Button identifier.

        is_bot (``bool``, *optional*):
            If True, show only Bots.

        is_premium (``bool``, *optional*):
            If True, show only Premium Users.

        max (``int``, *optional*):
            Maximum number of users to be returned.
            default 1.

        is_name_requested (``bool``, *optional*):
            If True, User name is requested.
            default True.

        is_username_requested (``bool``, *optional*):
            If True, User username is requested.
            default True.

        is_photo_requested (``bool``, *optional*):
            If True, User photo is requested.
            default True.    
    """

    def __init__(
        self,
        button_id: int=0,
        is_bot: bool=None,
        is_premium: bool=None,
        max: int=1,
        is_name_requested: bool=True,
        is_username_requested: bool=True,
        is_photo_requested: bool=True
    ):
        super().__init__()

        self.button_id = button_id
        self.is_bot = is_bot
        self.is_premium = is_premium
        self.max = max
        self.is_name_requested = is_name_requested
        self.is_username_requested = is_username_requested
        self.is_photo_requested = is_photo_requested
