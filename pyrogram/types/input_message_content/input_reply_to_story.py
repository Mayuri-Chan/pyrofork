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


class InputReplyToStory(Object):
    """Contains information about a target replied story.


    Parameters:
        peer (:obj:`~pyrogram.raw.types.InputPeer`):
            An InputPeer.

        story_id (``int``):
            Unique identifier for the target story.
    """

    def __init__(
        self, *,
        peer: "raw.types.InputPeer" = None,
        story_id: int = None
    ):
        super().__init__()

        self.peer = peer
        self.story_id = story_id

    def write(self):
        return raw.types.InputReplyToStory(
            peer=self.peer,
            story_id=self.story_id
        ).write()
