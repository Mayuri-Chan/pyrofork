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

from pyrofork import raw
from typing import List
from ..object import Object

class StoryViews(Object):
    """Contains information about a story viewers.


    Parameters:
        view_count (``int``):
            The count of stories viewers.

        recent_viewers (List of ``int``):
            List of user_id of recent stories viewers.
    """

    def __init__(
            self, *,
            view_count: int,
            recent_viewers: List[int] = None
    ):
        super().__init__()

        self.view_count = view_count
        self.recent_viewers = recent_viewers

    @staticmethod
    def _parse(storyviews: "raw.types.StoryViews") -> "StoryViews":
        return StoryViews(
            view_count=getattr(storyviews,"view_count", None),
            recent_viewers=getattr(storyviews,"recent_viewers", None)
        )
