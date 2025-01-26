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

from typing import Union

import pyrogram
from pyrogram import  raw, types


class TranscribeAudio:
    async def transcribe_audio(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int
    ) -> "types.TranscribedAudio":
        """Transcribes the audio of a voice message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the message containing the voice message.

        Returns:
            :obj:`~pyrogram.types.TranscribeAudio`: On success.
        """
        chat = await self.resolve_peer(chat_id)
        r = await self.invoke(
            raw.functions.messages.TranscribeAudio(
                peer=chat,
                msg_id=message_id
            )
        )

        return types.TranscribedAudio._parse(r)
