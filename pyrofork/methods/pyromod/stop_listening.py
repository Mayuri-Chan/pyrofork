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

from typing import List, Union
from pyrofork.types import Identifier

class StopListening:
    async def stop_listening(
        self: "pyrofork.Client",
        listener_type: "pyrofork.enums.ListenerTypes" = pyrofork.enums.ListenerTypes.MESSAGE,
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        """Stops all listeners that match the given identifier pattern.

        .. include:: /_includes/usable-by/users-bots.rst

        Uses :meth:`~pyrofork.Client.get_many_listeners_matching_with_identifier_pattern`.

        Parameters:
            listener_type (:obj:`~pyrofork.enums.ListenerTypes`, *optional*):
                The type of listener to stop listening for.
                Default to Message.

            chat_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The user ID to stop listening for.

            message_id (``int``, *optional*):
                The message ID to stop listening for.

            inline_message_id (``str``, *optional*):
                The inline message ID to stop listening for.
        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        listeners = self.get_many_listeners_matching_with_identifier_pattern(
            pattern, listener_type
        )

        for listener in listeners:
            await self.stop_listener(listener)
