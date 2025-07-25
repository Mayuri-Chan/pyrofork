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


from typing import List

from pyrogram import raw
from ..object import Object


class TodoTasksCompleted(Object):
    """One or more todo task/s has been flag as complete.

    Parameters:
        ids (List of ``int``):
            List of Unique identifier of the todo tasks.
    """

    def __init__(self, ids: List[int]):
        super().__init__()

        self.ids = ids

    @staticmethod
    def _parse(todo_completion: "raw.types.TodoCompletion") -> "TodoTasksCompleted":
        ids = [id for id in todo_completion.completed]
        return TodoTasksCompleted(
            ids=ids,
        )
