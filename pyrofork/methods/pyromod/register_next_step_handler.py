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
from typing import Callable, List, Optional, Union
from pyrofork.types import Identifier, Listener

class RegisterNextStepHandler:
    def register_next_step_handler(
        self: "pyrofork.Client",
        callback: Callable,
        filters: Optional[Filter] = None,
        listener_type: "pyrofork.enums.ListenerTypes" = pyrofork.enums.ListenerTypes.MESSAGE,
        unallowed_click_alert: bool = True,
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        """Registers a listener with a callback to be called when the listener is fulfilled.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            callback (``Callable``):
                The callback to call when the listener is fulfilled.

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

            message_id (``int``, *optional*):
                The message ID to listen for.

            inline_message_id (``str``, *optional*):
                The inline message ID to listen for.
        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        listener = Listener(
            callback=callback,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        self.listeners[listener_type].append(listener)
