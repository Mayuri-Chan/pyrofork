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

from typing import List
from pyrogram.types import ListenerTypes, Identifier, Listener

class GetManyListenersMatchingWithIdentifierPattern:
    def get_many_listeners_matching_with_identifier_pattern(
        self: "pyrogram.Client",
        pattern: Identifier,
        listener_type: ListenerTypes,
    ) -> List[Listener]:
        """
        Same of :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern` but returns a list of listeners instead of one.

        :param pattern: Same as :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern`.
        :param listener_type: Same as :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern`.
        :return: A list of listeners that match the given identifier pattern.
        """
        listeners = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                listeners.append(listener)
        return listeners
