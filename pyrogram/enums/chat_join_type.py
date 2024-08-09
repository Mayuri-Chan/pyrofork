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

from enum import auto

from .auto_name import AutoName


class ChatJoinType(AutoName):
    """How the service message :obj:`~pyrogram.enums.MessageServiceType.NEW_CHAT_MEMBERS` was used for the member to join the chat."""

    BY_ADD = auto()
    "A new member joined the chat via an invite link"

    BY_LINK = auto()
    "A new member joined the chat via an invite link"

    BY_REQUEST = auto()
    "A new member was accepted to the chat by an administrator"
