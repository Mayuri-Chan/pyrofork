#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.

import pyrogram
from pyrogram import raw, types, utils
from datetime import datetime
from ..object import Object

class ReadParticipant(Object):
    """Contains information about a read participant.

    Parameters:
        user (:obj:`~pyrogram.types.User`):
            User who read the message.

        date (:py:obj:`~datetime.datetime`):
            Date the message was read.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        user_id: "pyrogram.types.User",
        date: "datetime"
    ):
        super().__init__(client)

        self.user = user_id
        self.date = date

    @staticmethod
    async def _parse(
        client,
        read_participant: "raw.base.ReadParticipantDate"
    ) -> "ReadParticipant":
        return ReadParticipant(
            client=client,
            user_id=await client.get_users(read_participant.user_id),
            date=utils.timestamp_to_datetime(read_participant.date)
        )
