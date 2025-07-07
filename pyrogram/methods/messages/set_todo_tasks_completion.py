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

from typing import List, Union
from pyrogram import raw, types


class SetTodoTasksCompletion:
    async def set_todo_tasks_completion(
        self,
        chat_id: int | str,
        message_id: int,
        completed_ids: Union[int, List[int]] = None,
        incompleted_ids: Union[int, List[int]] = None
    ) -> "types.Message":
        """Set the completion status of one or more todo tasks.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Unique identifier of the message containing the todo list.

            completed_ids (``int`` | List of ``int``, *optional*):
                Unique identifier of the todo tasks to be marked as completed.
                If a list is provided, all tasks in the list will be marked as completed.

            incompleted_ids (``int`` | List of ``int``, *optional*):
                Unique identifier of the todo tasks to be marked as incomplete.
                If a list is provided, all tasks in the list will be marked as incomplete.
        """
        is_complete_iterable = None
        is_incomplete_iterable = None
        if completed_ids:
            is_complete_iterable = not isinstance(completed_ids, int)
        if incompleted_ids:
            is_incomplete_iterable = not isinstance(incompleted_ids, int)
        if not is_complete_iterable and not is_incomplete_iterable:
            raise ValueError("At least one of completed_ids or incompleted_ids must be provided.")

        r = await self.invoke(
            raw.functions.messages.ToggleTodoCompleted(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                completed=(completed_ids if is_complete_iterable else [completed_ids]) if completed_ids else [],
                incompleted=(incompleted_ids if is_incomplete_iterable else [incompleted_ids]) if incompleted_ids else []
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage,
                              raw.types.UpdateBotNewBusinessMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                )
