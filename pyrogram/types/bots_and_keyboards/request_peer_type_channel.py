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


class RequestPeerTypeChannel(Object):
    """Object used to request clients to send a channel identifier.

    Parameters:
        is_creator (``bool``, *optional*):
            If True, show only Channel which user is the owner.

        is_username (``bool``, *optional*):
            If True, show only Channel which has username.
    """ # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        is_creator: bool=None,
        is_username: bool=None,
        max: int=1
    ):
        super().__init__()

        self.is_creator = is_creator
        self.is_username = is_username
        self.max = max
