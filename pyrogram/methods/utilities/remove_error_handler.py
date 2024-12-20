#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from __future__ import annotations
from collections.abc import Iterable
import pyrogram


class RemoveErrorHandler:
    def remove_error_handler(
        self: pyrogram.Client,
        exception: type[Exception] | Iterable[type[Exception]] = Exception,
    ):
        """Remove a previously registered error handler using exception classes.

        Parameters:
            exception (``Exception`` | Iterable of ``Exception``, *optional*):
                The error(s) for handlers to be removed. Defaults to Exception.
        """
        to_remove = [
            handler
            for handler in self.dispatcher.error_handlers
            if handler.check_remove(exception)
        ]
        for handler in to_remove:
            self.dispatcher.error_handlers.remove(handler)
