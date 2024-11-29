#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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
from ..object import Object
from typing import List, Optional


class PollOption(Object):
    """Contains information about one answer option in a poll.

    Parameters:
        text (``str``):
            Option text, 1-100 characters.

        voter_count (``int``, *optional*):
            Number of users that voted for this option.
            Equals to 0 until you vote.

        data (``bytes``, *optional*):
            The data this poll option is holding.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities like usernames, URLs, bot commands, etc. that appear in the option text.
    """

    def __init__(
        self: "pyrogram.Client",
        text: str,
        voter_count: int = 0,
        data: bytes = None,
        entities: Optional[List["pyrogram.types.MessageEntity"]] = None,
    ):
        super().__init__(self)

        self.text = text
        self.voter_count = voter_count
        self.data = data
        self.entities = entities

    async def write(self, client, i):
        option, entities = (await pyrogram.utils.parse_text_entities(client, self.text, None, self.entities)).values()
        return pyrogram.raw.types.PollAnswer(
            text=pyrogram.raw.types.TextWithEntities(
                text=option,
                entities=entities or []
            ),
            option=bytes([i])
        )
