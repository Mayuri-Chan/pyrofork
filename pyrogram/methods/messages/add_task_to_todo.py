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

from pyrogram import raw, types, utils
from typing import Union, List


class AddTaskToTodo:
    async def add_task_to_todo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: Union[int, str],
        tasks: List["types.InputTodoTask"],
        parse_mode: str = None
    ) -> "types.Message":
        """Add tasks to a todo list.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel.

            message_id (``int`` | ``str``):
                Unique identifier for the target message or username of the target channel.

            tasks (List of :obj:`~pyrogram.types.InputTodoTask`):
                List of tasks to be added to the todo list.

            parse_mode (``str``, *optional*):
                The parse mode to use for formatting the text.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Entities in the title of the todo list.
        """
        tasks_list = []
        get_message = await self.get_messages(chat_id, message_id)
        if not isinstance(get_message, types.Message):
            raise ValueError("The message must be a valid Message object.")
        todo_list = get_message.todo
        last_task_id = max((task.id for task in todo_list.tasks), default=0)
        for i, task in enumerate(tasks):
            task_title, task_entities = (await utils.parse_text_entities(self, task.title, parse_mode, task.entities)).values()
            tasks_list.append(
                raw.types.TodoItem(
                    id=last_task_id + i + 1,
                    title=raw.types.TextWithEntities(
                        text=task_title,
                        entities=task_entities or []
                    )
                )
            )

        r = await self.invoke(
            raw.functions.messages.AppendTodoList(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                list=tasks_list
            )
        )

        for update in r.updates:
            if isinstance(update, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage,
                              raw.types.UpdateBotNewBusinessMessage)):
                return types.Message._parse(self, update.message, update, r.users, r.chats)
