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

import logging

import pyrofork
from pyrofork import raw
from pyrofork import types
from pyrofork.utils import compute_password_check

log = logging.getLogger(__name__)


class CheckPassword:
    async def check_password(
        self: "pyrofork.Client",
        password: str
    ) -> "types.User":
        """Check your Two-Step Verification password and log in.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            password (``str``):
                Your Two-Step Verification password.

        Returns:
            :obj:`~pyrofork.types.User`: On success, the authorized user is returned.

        Raises:
            BadRequest: In case the password is invalid.
        """
        r = await self.invoke(
            raw.functions.auth.CheckPassword(
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()),
                    password
                )
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
