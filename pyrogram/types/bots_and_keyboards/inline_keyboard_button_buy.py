#  Pyrofork - Telegram MTProto API Client Library for Python
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

from ..object import Object

from pyrogram import raw

class InlineKeyboardButtonBuy(Object):
    """One button of the inline keyboard.
    For simple invoice buttons.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.
    """

    def __init__(
        self,
        text: str
    ):
        super().__init__()

        self.text = str(text)

    @staticmethod
    def read(b):
        return InlineKeyboardButtonBuy(
            text=b.text
        )

    async def write(self, _: "pyrogram.Client"):
        return raw.types.KeyboardButtonBuy(
            text=self.text
        )
