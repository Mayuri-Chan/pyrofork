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


class RequestPeerTypeChat(Object):
    """Object used to request clients to send a chat identifier.

    Parameters:
        is_creator (``bool``, *optional*):
            If True, show only Chat which user is the owner.

        is_bot_participant (``bool``, *optional*):
            If True, show only Chat where bot is a participant.

        is_username (``bool``, *optional*):
            If True, show only Chat which has username.

        is_forum (``bool``, *optional*):
            If True, show only Chat which is a forum.
    """ # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        is_creator: bool=None,
        is_bot_participant: bool=None,
        is_username: bool=None,
        is_forum: bool=None,
        max: int=1
    ):
        super().__init__()

        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.is_username = is_username
        self.is_forum = is_forum
        self.max = max
