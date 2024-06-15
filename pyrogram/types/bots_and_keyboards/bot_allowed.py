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

from typing import Optional

from pyrogram import raw, types
from ..object import Object


class BotAllowed(Object):
    
    """Contains information about a allowed bot.

    Parameters:
        attach_menu (``bool``, *optional*):
            True, if the bot can attach to menu.

        from_request (``bool``, *optional*):
            True, if the bot is allowed from request.

        domain (``str``, *optional*):
            The domain of the bot.

        app (:obj:`~pyrogram.types.BotApp`, *optional*):
            The app of the bot.
    """
    
    def __init__(
        self,
        *,
        attach_menu: Optional[bool] = None,
        from_request: Optional[bool] = None,
        domain: Optional[str] = None,
        app: Optional["types.BotApp"] = None
    ):
        super().__init__()
    
        self.attach_menu = attach_menu
        self.from_request = from_request
        self.domain = domain
        self.app = app
    
    @staticmethod
    def _parse(client: "pyrogram.Client", bot_allowed: "raw.types.BotAllowed") -> "BotAllowed":
        bot_app = getattr(bot_allowed, "app", None)
        return BotAllowed(
            attach_menu=getattr(bot_allowed, "attach_menu", None),
            from_request=getattr(bot_allowed, "from_request", None),
            domain=getattr(bot_allowed, "domain", None),
            app=types.BotApp._parse(client, bot_app) if bot_app is not None else None
        )
