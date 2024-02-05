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

log = logging.getLogger(__name__)


class LogOut:
    async def log_out(
        self: "pyrofork.Client",
    ):
        """Log out from Telegram and delete the *\\*.session* file.

        When you log out, the current client is stopped and the storage session deleted.
        No more API calls can be made until you start the client and re-authorize again.

        .. include:: /_includes/usable-by/users-bots.rst

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Log out.
                app.log_out()
        """
        await self.invoke(raw.functions.auth.LogOut())
        await self.stop()
        await self.storage.delete()

        return True
