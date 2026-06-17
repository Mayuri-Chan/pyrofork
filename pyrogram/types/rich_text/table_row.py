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

from typing import Optional, List

import pyrogram
from pyrogram import raw, types
from ..object import Object


class TableRow(Object):
    """A row in a table page block.

    Parameters:
        cells (List of :obj:`~pyrogram.types.TableCell`):
            The cells contained in this row.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        cells: List[types.TableCell],
    ):
        super().__init__(client)
        self.cells = cells

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        row: "raw.types.PageTableRow"
    ) -> Optional["TableRow"]:
        return TableRow(
            client=client,
            cells=[types.TableCell._parse(client, getattr(row, "cells", []))],
        )
