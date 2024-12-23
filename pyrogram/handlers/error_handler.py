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
from typing import Callable

from .handler import Handler

import pyrogram
from pyrogram.types import Update


class ErrorHandler(Handler):
    """The Error handler class. Used to handle errors.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_error` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Error arrives. It takes *(client, error)*
            as positional arguments (look at the section below for a detailed description).

        exceptions (``Exception`` | Iterable of ``Exception``, *optional*):
            Pass one or more exception classes to allow only a subset of errors to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the error handler.

        update (:obj:`~pyrogram.Update`):
            The update that caused the error.

        error (``Exception``):
            The error that was raised.
    """

    def __init__(
        self,
        callback: Callable,
        exceptions: type[Exception] | Iterable[type[Exception]] | None = None,
    ):
        self.exceptions = (
            tuple(exceptions)
            if isinstance(exceptions, Iterable)
            else (exceptions,)
            if exceptions
            else (Exception,)
        )
        super().__init__(callback)

    async def check(self, client: pyrogram.Client, update: Update, exception: Exception) -> bool:
        if isinstance(exception, self.exceptions):
            await self.callback(client, update, exception)
            return True
        return False

    def check_remove(self, error: type[Exception] | Iterable[type[Exception]]) -> bool:
        return isinstance(error, self.exceptions)
