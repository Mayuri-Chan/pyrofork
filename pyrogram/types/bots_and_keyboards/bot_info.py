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

from pyrogram import raw

from ..object import Object


class BotInfo(Object):
    """A bot Information.

    Parameters:
        name (``str``):
            The bot name.
        
        about (``str``):
            The bot bio.

        description (``str``):
            Description of the bot;
    """

    def __init__(self, name: str, about: str, description: str):
        super().__init__()

        self.name = name
        self.about = about
        self.description = description

    
    @staticmethod
    def _parse(bot_info: "raw.types.bots.BotInfo") -> "BotInfo":
        return BotInfo(
            name=getattr(bot_info,"name", None),
            about=getattr(bot_info,"about", None),
            description=getattr(bot_info,"description", None)
        )
