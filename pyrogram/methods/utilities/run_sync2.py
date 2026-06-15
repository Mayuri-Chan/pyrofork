"""PyroFork async utils"""
# Copyright (C) 2020 - 2023  UserbotIndo Team, <https://github.com/userbotindo.git>
# Copyright (C) 2022-present  Mayuri-Chan, <https://github.com/Mayuri-Chan.git>
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

from pyrogram import utils
from typing import Any, Callable, TypeVar, ParamSpec

class RunSync2:
    P = ParamSpec("P")
    R = TypeVar("R")

    async def run_sync2(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """Runs the given sync function (optionally with arguments) on a separate thread.

        This method is identical to :meth:`~pyrogram.Client.run_sync` but utilizes ``ParamSpec``
        to provide strict parameter type inference for modern type checkers. It is useful for 
        blocking operations where type safety is prioritized, such as PyTesseract OCR tasks.

        Parameters:
            func (``Callable``):
                Sync function to run.

            *args (``any``, *optional*):
                Function arguments.

            **kwargs (``any``, *optional*):
                Function keyword arguments.

        Returns:
                ``any``: The function result.

        Example:
            .. code-block:: python

                import pytesseract
                from PIL import Image
                from pyrogram import Client

                app = Client("my_account")

                def extract_text(image_path: str):
                    return pytesseract.image_to_string(Image.open(image_path))

                async def main():
                    async with app:
                        text = await app.run_sync2(extract_text, "image.jpg")
                        print(text)

                app.run(main())
        """

        return await utils.run_sync2(func, *args, **kwargs)
