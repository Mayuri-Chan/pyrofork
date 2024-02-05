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
from pyrofork.types import Listener

class RemoveListener:
    def remove_listener(
        self: "pyrofork.Client",
        listener: Listener
    ):
        """Removes a listener from the :meth:`~pyrofork.Client.listeners` dictionary.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            listener (:obj:`~pyrofork.types.Listener`):
                The listener to remove.
        """
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
