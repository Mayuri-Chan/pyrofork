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


class RequestPeerTypeChat(Object):
    """Object used to tell clients to request a suitable chat.

    The identifier of the selected chat will be shared with the bot when the corresponding button is pressed.

    Parameters:
        creator (``bool``, *optional*):
            Pass True to request a chat owned by the user.
            Otherwise, no additional restrictions are applied.

        bot_participant (``bool``, *optional*):
            Pass True to request a chat with the bot as a member.
            Otherwise, no additional restrictions are applied.

        has_username (``bool``, *optional*):
            Pass True to request a supergroup or a channel with a username, pass False to request a chat without a username.
            If not specified, no additional restrictions are applied.

        is_forum (``bool``, *optional*):
            Pass True to request a forum supergroup, pass False to request a non-forum chat.
            If not specified, no additional restrictions are applied.

        user_admin_rights (:obj:`~pyrogram.types.ChatPermissions`, *optional*):
            A JSON-serialized object listing the required administrator rights of the user in the chat.
            If not specified, no additional restrictions are applied.

        bot_admin_rights (:obj:`~pyrogram.types.ChatPermissions`, *optional*):
            A JSON-serialized object listing the required administrator rights of the bot in the chat. The rights must be a subset of user_administrator_rights.
            If not specified, no additional restrictions are applied.
    """

    def __init__(
        self,
        creator: bool = None,
        bot_participant: bool = None,
        has_username: bool = None,
        is_forum: bool = None,
        user_admin_rights: "types.ChatPermissions" = None,
        bot_admin_rights: "types.ChatPermissions" = None
    ):
        super().__init__()

        self.creator = creator
        self.bot_participant = bot_participant
        self.has_username = has_username
        self.is_forum = is_forum
        self.user_admin_rights = user_admin_rights
        self.bot_admin_rights = bot_admin_rights

    async def write(self, _: "pyrogram.Client"):
        return raw.types.RequestPeerTypeChat(
            creator=self.creator or None,
            bot_participant=self.bot_participant or None,
            has_username=self.has_username or None,
            forum=self.is_forum or None,
            user_admin_rights=self.user_admin_rights or None,
            bot_admin_rights=self.bot_admin_rights or None
        )
