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

from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import pyrofork

from .identifier import Identifier

@dataclass
class Listener:
    """Designed to manage and handle different types of listeners used in pyromod.
    It enables you to wait for specific events like messages or callback queries and provides mechanisms for defining the conditions and filters that trigger these listeners.

    Parameters:
        listener_type (:obj:`~pyrofork.enums.ListenerTypes`):
            The type of listener that specifies the event you want to listen for.
            It can be either a “message” or a “callback_query.”

        filters (:meth:`~pyrofork.filters.Filter`):
            The chat ID to match. If None, it is not considered for matching.

        unallowed_click_alert (``bool``):
            A flag that determines whether to send an alert if a button click event doesn’t match the filter conditions.
            Setting this to True will send an alert message to the user in such cases.

        identifier (:obj:`~pyrofork.types.Identifier`):
            An :obj:`~pyrofork.types.Identifier` instance that defines the criteria for the event.
            It includes properties like chat_id, message_id, from_user_id, and inline_message_id that you want to match against the incoming event.

        future (:obj:`~asyncio.Future`, *optional*):
            A :obj:`~asyncio.Future` object representing the asynchronous task that waits for the event.
            When the event occurs, the :obj:`~asyncio.Future` will be resolved, and the listener will be able to proceed.

        callback (``Callable``, *optional*):
            The callback to call when the listener is fulfilled.
    """
    listener_type: pyrofork.enums.ListenerTypes
    filters: "pyrofork.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None
