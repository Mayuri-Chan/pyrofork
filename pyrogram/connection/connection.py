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

import asyncio
import logging
from typing import Optional, Type

from .transport import TCP, TCPAbridged
from ..session.internals import DataCenter

log = logging.getLogger(__name__)


class Connection:
    MAX_CONNECTION_ATTEMPTS = 3

    def __init__(
        self,
        dc_id: int,
        test_mode: bool,
        ipv6: bool,
        alt_port: bool,
        proxy: dict,
        media: bool = False,
        protocol_factory: Type[TCP] = TCPAbridged
    ) -> None:
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.alt_port = alt_port
        self.proxy = proxy
        self.media = media
        self.protocol_factory = protocol_factory

        self.address = DataCenter(dc_id, test_mode, ipv6, alt_port, media)
        self.protocol: Optional[TCP] = None

    async def connect(self) -> None:
        for i in range(Connection.MAX_CONNECTION_ATTEMPTS):
            self.protocol = self.protocol_factory(ipv6=self.ipv6, proxy=self.proxy)

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning("Unable to connect due to network issues: %s", e)
                await self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info("Connected! %s DC%s%s - IPv%s",
                         "Test" if self.test_mode else "Production",
                         self.dc_id,
                         " (media)" if self.media else "",
                         "6" if self.ipv6 else "4")
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise ConnectionError

    async def close(self) -> None:
        await self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes) -> None:
        await self.protocol.send(data)

    async def recv(self) -> Optional[bytes]:
        return await self.protocol.recv()
