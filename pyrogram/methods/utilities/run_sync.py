"""PyroFork async utils"""
# Copyright (C) 2020 - 2023  UserbotIndo Team, <https://github.com/userbotindo.git>
# Copyright (C) 2023  Mayuri-Chan, <https://github.com/Mayuri-Chan.git>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import functools
from pyrogram import utils
from typing import Any, Callable, TypeVar

class RunSync:
    Result = TypeVar("Result")

    async def run_sync(self, func: Callable[..., Result], *args: Any, **kwargs: Any) -> Result:
        """Runs the given sync function (optionally with arguments) on a separate thread.

        Parameters:
            func (``Callable``):
                Sync function to run.

            \\*args (``any``, *optional*):
                Function argument.

            \\*\\*kwargs (``any``, *optional*):
                Function extras arguments.

        Returns:
                ``any``: The function result.
        """

        return await utils.run_sync(func, *args, **kwargs)
