#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import functools
import logging

import pyrogram

from typing import Union

log = logging.getLogger(__name__)


class Listen:
    async def listen(
        self: "pyrogram.Client",
        chat_id: Union[str, int],
        filters=None,
        timeout: int = None
    ):
        """Awaits for a new message in the specified chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            timeout (``int``, *optional*):
                The waiting timeout.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, text message is returned.

        Example:
            .. code-block:: python

                await Client.send_message(chat_id, "Your name:")
                answer = await Client.listen(chat_id)
                name = answer.text
        """
        if type(chat_id) != int:
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        future = self.loop.create_future()
        future.add_done_callback(
            functools.partial(self.clear_listener, chat_id)
        )
        self.listening.update({
            chat_id: {"future": future, "filters": filters}
        })
        return await asyncio.wait_for(future, timeout)

    def clear_listener(
        self: "pyrogram.Client",
        chat_id: Union[str, int],
        future
    ):
        if chat_id in self.listening and future == self.listening[chat_id]["future"]:
            self.listening.pop(chat_id, None)

    def cancel_listener(
        self: "pyrogram.Client",
        chat_id: Union[str, int]
    ):
        listener = self.listening.get(chat_id)
        if not listener or listener['future'].done():
            return

        listener['future'].set_exception(ListenerCanceled())
        self.clear_listener(chat_id, listener['future'])
