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

from typing import Union

import pyrogram
from pyrogram import raw


class SetBotInfo:
    async def set_bot_info(
        self: "pyrogram.Client",
        lang_code: str,
        bot: Union[int, str] = None,
        name: str = None,
        about: str = None,
        description: str = None
    ) -> bool:
        """Get the bot info in given language.

        .. include:: /_includes/usable-by/users-bots.rst

        Note:
            For normal bot you can only use this method to self.
            For userbot you can only use this method if you are the owner of target bot.

        Parameters:
            lang_code ``str``:
                A two-letter ISO 639-1 language code.
            bot (``int`` | ``str``, *optional*) :
                Unique identifier (int) or username (str) of the target bot.

            name (``str``, *optional*):
                The bot name.
            
            about (``str``, *optional*):
                The bot bio.

            description (``str``, *optional*):
                Description of the bot;
        """
        peer = None
        if bot:
            peer = await self.resolve_peer(bot)
        r = await self.invoke(raw.functions.bots.SetBotInfo(lang_code=lang_code, bot=peer, name=name, about=about, description=description))
        return bool(r)
