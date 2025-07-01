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

from time import time

import pyrogram
from pyrogram import raw


class Ping:
    async def ping(self: "pyrogram.Client"):
        """Measure the round-trip time (RTT) to the Telegram server.

        The ping method sends a request to the Telegram server and measures the time it takes to receive a response.
        This can be useful for monitoring network latency and ensuring a stable connection to the server.

        Returns:
            float: The round-trip time in milliseconds (ms).

        Example:
            .. code-block:: python

                latency = await app.ping()
                print(f"Ping: {latency} ms")
        """
        start_time = time()
        await self.invoke(
            raw.functions.ping.Ping(ping_id=self.rnd_id()),
        )
        return round((time() - start_time) * 1000.0, 3)
