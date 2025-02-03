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

from pyrogram import  raw
from ..object import Object


class TranscribedAudio(Object):
    """Transcribes the audio of a voice message.
    
    Parameters:
        transcription_id (``int``):
            Unique identifier of the transcription.

        text (``str``):
            Transcribed text.

        pending (``bool``, *optional*):
            Whether the transcription is pending.

        trial_remains_num (``int``, *optional*):
            Number of trials remaining.

        trial_remains_until_date (``int``, *optional*):
            Date the trial remains until.
    """

    def __init__(
        self,
        *,
        transcription_id: int,
        text: str,
        pending: bool = None,
        trial_remains_num: int = None,
        trial_remains_until_date: int = None
    ):
        self.transcription_id = transcription_id
        self.text = text
        self.pending = pending
        self.trial_remains_num = trial_remains_num
        self.trial_remains_until_date = trial_remains_until_date

    @staticmethod
    def _parse(transcribe_result: "raw.types.messages.TranscribedAudio") -> "TranscribeAudio":
        return TranscribedAudio(
            transcription_id=transcribe_result.transcription_id,
            text=transcribe_result.text,
            pending=transcribe_result.pending,
            trial_remains_num=transcribe_result.trial_remains_num,
            trial_remains_until_date=transcribe_result.trial_remains_until_date
        )
