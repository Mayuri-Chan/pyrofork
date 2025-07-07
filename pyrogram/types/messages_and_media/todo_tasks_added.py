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

import pyrogram

from pyrogram import raw, types
from ..object import Object


class TodoTasksAdded(Object):
    """A todo task added to a todo list.

    Parameters:
        task (:obj:`~pyrogram.types.TodoTask`):
            The added todo task.
    """

    def __init__(self, tasks: "types.TodoTask"):
        super().__init__()

        self.tasks = tasks

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        todo_task_added: "raw.types.MessageActionTodoAppendTasks"
    ) -> "TodoTasksAdded":
        return TodoTasksAdded(
            tasks=[types.TodoTask._parse(client, task, {}, {}) for task in todo_task_added.list]
        )
