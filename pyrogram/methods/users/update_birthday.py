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
from pyrogram import raw, types


class UpdateBirthday:
    async def update_birthday(
        self: "pyrogram.Client",
        day: int,
        month: int,
        year: int = None
    ) -> bool:
        """Update your birthday details.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            day (``int``):
                Day of birth.

            month (``int``):
                Month of birth.

            year (``int``, *optional*):
                Year of birth.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your birthday to 1st January 2000
                # 1874/01/01(YMD) is the earliest date, earlier will raise 400 Bad Request BIRTHDAY_INVALID.
                await app.update_birthday(day=1, month=1, year=2000)
        """
        birthday = types.Birthday(day=day, month=month, year=year)
        birthday = await birthday.write()

        r = await self.invoke(raw.functions.account.UpdateBirthday(birthday=birthday))
        if r:
            return True
        return False
