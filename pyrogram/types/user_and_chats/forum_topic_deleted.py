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

from pyrogram import raw, types
from typing import Union
from ..object import Object


class ForumTopicDeleted(Object):
    """A deleted forum topic.

    Parameters:
        id (``Integer``):
            Id of the topic
    """

    def __init__(
        self,
        *,
        id: int
    ):
        super().__init__()

        self.id = id

    @staticmethod
    def _parse(forum_topic: "raw.types.ForumTopicDeleted") -> "ForumTopicDeleted":
        return ForumTopicDeleted(
            id=getattr(forum_topic,"id", None)
        )
