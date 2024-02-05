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

from typing import Optional

from pyrofork import raw
from .reaction_type import ReactionType
from ..object import Object

class ReactionCount(Object):
    """Represents a reaction added to a message along with the number of times it was added.

    Parameters:

        type (:obj:`~pyrofork.types.ReactionType`):
            Reaction type.

        total_count (``int``):
            Total reaction count.

        chosen_order (``int``):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        type: ReactionType,
        total_count: int,
        chosen_order: int
    ):
        super().__init__()
        self.type = type
        self.total_count = total_count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        update: "raw.types.ReactionCount",
    ) -> Optional["ReactionCount"]:
        return ReactionCount(
            type=ReactionType._parse(
                update.reaction
            ),
            total_count=update.count,
            chosen_order=update.chosen_order
        )
