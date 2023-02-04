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

from pyrogram import raw, types
from ..object import Object


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        request_chat (:obj:`~pyrogram.types.RequestPeerTypeChat`, *optional*):
            If specified, pressing the button will open a list of suitable chats.
            Tapping on a chat will send its identifier to the bot in a “chat_shared” service message.
            Available in private chats only.

        request_user (:obj:`~pyrogram.types.RequestPeerTypeUser`, *optional*):
            If specified, pressing the button will open a list of suitable users.
            Tapping on any user will send their identifier to the bot in a “user_shared” service message.
            Available in private chats only.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

    """

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        request_chat: "types.RequestPeerTypeChat" = None,
        request_user: "types.RequestPeerTypeUser" = None,
        web_app: "types.WebAppInfo" = None
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_chat = request_chat
        self.request_user = request_user
        self.web_app = web_app

    @staticmethod
    def read(b):
        if isinstance(b, raw.types.KeyboardButton):
            return b.text

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                )
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPeer):
            if isinstance(b.peer_type, raw.types.RequestPeerTypeUser):
                return KeyboardButton(
                    text=b.text,
                    request_user=types.RequestPeerTypeUser(
                        is_bot=b.peer_type.bot,
                        is_premium=b.peer_type.premium
                    )
                )
            return KeyboardButton(
                text=b.text,
                request_chat=types.RequestPeerTypeChat(
                    creator=b.peer_type.creator,
                    bot_participant=b.peer_type.bot_participant,
                    has_username=b.peer_type.has_username,
                    is_forum=b.peer_type.forum,
                    user_admin_rights=b.peer_type.user_admin_rights,
                    bot_admin_rights=b.peer_type.bot_admin_rights
                )
            )

    def write(self):
        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text)
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(text=self.text, url=self.web_app.url)
        elif self.request_chat:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeChat(
                    creator=self.request_chat.creator or None,
                    bot_participant=self.request_chat.bot_participant or None,
                    has_username=self.request_chat.has_username or None,
                    forum=self.request_chat.forum or None,
                    user_admin_rights=self.request_chat.user_admin_rights or None,
                    bot_admin_rights=self.request_chat.bot_admin_rights or None
                )
            )
        elif self.request_user:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeUser(
                    bot=self.request_user.is_bot or None,
                    premium=self.request_user.is_premium or None
                )
            )
        else:
            return raw.types.KeyboardButton(text=self.text)
