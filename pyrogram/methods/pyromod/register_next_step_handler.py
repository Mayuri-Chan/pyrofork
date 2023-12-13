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

import pyrogram

from pyrogram.filters import Filter
from typing import Callable, List, Optional, Union
from pyrogram.types import ListenerTypes, Identifier, Listener

class RegisterNextStepHandler:
    def register_next_step_handler(
        self: "pyrogram.Client",
        callback: Callable,
        filters: Optional[Filter] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        unallowed_click_alert: bool = True,
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        """
        Registers a listener with a callback to be called when the listener is fulfilled.

        :param callback: The callback to call when the listener is fulfilled.
        :param filters: Same as :meth:`pyromod.types.Client.listen`.
        :param listener_type: Same as :meth:`pyromod.types.Client.listen`.
        :param unallowed_click_alert: Same as :meth:`pyromod.types.Client.listen`.
        :param chat_id: Same as :meth:`pyromod.types.Client.listen`.
        :param user_id: Same as :meth:`pyromod.types.Client.listen`.
        :param message_id: Same as :meth:`pyromod.types.Client.listen`.
        :param inline_message_id: Same as :meth:`pyromod.types.Client.listen`.
        :return: ``void``
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
