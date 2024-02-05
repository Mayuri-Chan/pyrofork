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

import pyrofork

from pyrofork.filters import Filter
from typing import List, Optional, Union

class Ask:
    async def ask(
        self: "pyrofork.Client",
        chat_id: Union[Union[int, str], List[Union[int, str]]],
        text: str,
        filters: Optional[Filter] = None,
        listener_type: "pyrofork.enums.ListenerTypes" = pyrofork.enums.ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
        *args,
        **kwargs,
    ):
        """Send a message then listen for a message, callback query, etc.

        Message:

        .. include:: /_includes/usable-by/users-bots.rst

        CallbackQuery:

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``):
                Unique identifier (int) or username (str) of the target chat.

            text (``str``):
                Text of the message to be sent.

            user_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The user ID to listen for.

            filters (:obj:`~pyrofork.filters`, *optional*):
                A filter to check the incoming message against.

            listener_type (:obj:`~pyrofork.enums.ListenerTypes`, *optional*):
                The type of listener to listen for.
                Default to Message.

            timeout (``int``, *optional*):
                The maximum amount of time to wait for a message.

            unallowed_click_alert (``bool``, *optional*):
                Whether to alert the user if they click a button that doesn’t match the filters.
                Default to True.

            inline_message_id (``str``, *optional*):
                The inline message ID to listen for.

        Returns:
            :obj:`~pyrofork.types.Message` | :obj:`~pyrofork.types.CallbackQuery`: On success, a message/callbackquery is returned.

        Example:
            .. code-block:: python

                await app.ask(chat_id, "Tell me your name:")
        """
        sent_message = None
        if text and isinstance(text, str):
            chat_to_ask = chat_id[0] if isinstance(chat_id, list) else chat_id
            sent_message = await self.send_message(chat_to_ask, text, *args, **kwargs)

        response = await self.listen(
            filters=filters,
            listener_type=listener_type,
            timeout=timeout,
            unallowed_click_alert=unallowed_click_alert,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        if response:
            response.sent_message = sent_message

        return response
