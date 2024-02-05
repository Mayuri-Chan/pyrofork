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

from typing import List
from pyrofork.types import Identifier, Listener

class GetManyListenersMatchingWithIdentifierPattern:
    def get_many_listeners_matching_with_identifier_pattern(
        self: "pyrofork.Client",
        pattern: Identifier,
        listener_type: "pyrofork.enums.ListenerTypes",
    ) -> List[Listener]:
        """Gets multiple listener that matches the given identifier pattern.

        .. include:: /_includes/usable-by/users-bots.rst

        The difference from :meth:`~pyrofork.Client.get_listener_matching_with_data` is that this method
        intends to get a listener by passing partial info of the listener identifier, while the other method
        intends to get a listener by passing the full info of the update data, which the listener should match with.

        Parameters:
            pattern (:obj:`~pyrofork.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~pyrofork.enums.ListenerTypes`):
                The type of listener to get.

        Returns:
            List of :obj:`~pyrofork.types.Listener`: On success, a list of Listener is returned.
        """
        listeners = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                listeners.append(listener)
        return listeners
