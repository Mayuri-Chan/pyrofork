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

from typing import List, Union

import pyrogram
from pyrogram import raw


class GetSimilarBots:
    async def get_similar_bots(
        self: "pyrogram.Client",
        bot: Union[int, str]
    ) -> List["pyrogram.types.User"]:
        """Get a list of bots similar to the target bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target bot.

        Returns:
            List of :obj:`~pyrogram.types.User`: On success.
        """
        peer = await self.resolve_peer(bot)
        r = await self.invoke(raw.functions.bots.GetBotRecommendations(bot=peer))
        return pyrogram.types.List([
            pyrogram.types.User._parse(self, u)
            for u in r.users
        ])
