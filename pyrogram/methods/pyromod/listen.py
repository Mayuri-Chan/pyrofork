#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2020 Cezar H. <https://github.com/usernein>
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

import asyncio
import inspect
import pyrogram

from pyrogram.errors import ListenerTimeout
from pyrogram.filters import Filter
from typing import List, Optional, Union
from pyrogram.types import ListenerTypes, Identifier, Listener
from pyrogram.utils import PyromodConfig

class Listen:
    async def listen(
        self: "pyrogram.Client",
        filters: Optional[Filter] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        """
        Creates a listener and waits for it to be fulfilled.

        :param filters: A filter to check if the listener should be fulfilled.
        :param listener_type: The type of listener to create. Defaults to :attr:`pyromod.types.ListenerTypes.MESSAGE`.
        :param timeout: The maximum amount of time to wait for the listener to be fulfilled. Defaults to ``None``.
        :param unallowed_click_alert: Whether to alert the user if they click on a button that is not intended for them. Defaults to ``True``.
        :param chat_id: The chat ID(s) to listen for. Defaults to ``None``.
        :param user_id: The user ID(s) to listen for. Defaults to ``None``.
        :param message_id: The message ID(s) to listen for. Defaults to ``None``.
        :param inline_message_id: The inline message ID(s) to listen for. Defaults to ``None``.
        :return: The Message or CallbackQuery that fulfilled the listener.
        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        listener = Listener(
            future=future,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        future.add_done_callback(lambda _future: self.remove_listener(listener))

        self.listeners[listener_type].append(listener)

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(PyromodConfig.timeout_handler):
                if inspect.iscoroutinefunction(PyromodConfig.timeout_handler.__call__):
                    await PyromodConfig.timeout_handler(pattern, listener, timeout)
                else:
                    await self.loop.run_in_executor(
                        None, PyromodConfig.timeout_handler, pattern, listener, timeout
                    )
            elif PyromodConfig.throw_exceptions:
                raise ListenerTimeout(timeout)
