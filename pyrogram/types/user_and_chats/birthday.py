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

from typing import Optional, Union

from pyrogram import raw
from pyrogram import enums
from ..object import Object


class Birthday(Object):
    """User Date of birth.

    Parameters:
        day (``int``):
            Day of birth.

        month (``int``):
            Month of birth.

        year (``int``):
            Year of birth.
    """

    def __init__(
        self,
        *,
        day: int,
        month: int,
        year: int
    ):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(birthday: "raw.types.Birthday" = None) -> "Birthday":
        return Birthday(
            day=birthday.day,
            month=birthday.month,
            year=birthday.year
        )

    async def write(self) -> "raw.types.Birthday":
        return raw.types.Birthday(
            day=self.day,
            month=self.month,
            year=self.year
        )
