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
import base64
import ipaddress
import socket
import struct
from typing import Tuple, Dict, TypedDict, Optional, Union

import socks

proxy_type_by_scheme: Dict[str, int] = {
    "SOCKS4": socks.SOCKS4,
    "SOCKS5": socks.SOCKS5,
    "HTTP": socks.HTTP,
}


class Proxy(TypedDict):
    scheme: str
    hostname: str
    port: int
    username: Optional[str]
    password: Optional[str]


class ProxyError(Exception):
    """Base exception for proxy-related errors."""


class AuthenticationError(ProxyError):
    """Authentication failed."""


class ConnectionError(ProxyError):
    """Connection failed."""


class SOCKS5Handler:
    """Handles SOCKS5 proxy operations."""

    @staticmethod
    async def negotiate_auth(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        username: Optional[str],
        password: Optional[str],
        timeout: int,
    ) -> int:
        """Handle SOCKS5 authentication negotiation."""
        auth_methods = b"\x05\x02\x00\x02" if username and password else b"\x05\x01\x00"

        writer.write(auth_methods)
        await writer.drain()

        response = await asyncio.wait_for(reader.read(2), timeout)
        if len(response) != 2 or response[0] != 0x05:
            raise ConnectionError("Invalid SOCKS5 response")

        return response[1]

    @staticmethod
    async def authenticate(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        username: str,
        password: str,
        timeout: int,
    ) -> None:
        """Perform username/password authentication."""
        username_bytes = username.encode("utf-8")
        password_bytes = password.encode("utf-8")
        auth_request = (
            bytes([0x01, len(username_bytes)])
            + username_bytes
            + bytes([len(password_bytes)])
            + password_bytes
        )

        writer.write(auth_request)
        await writer.drain()

        auth_response = await asyncio.wait_for(reader.read(2), timeout)
        if len(auth_response) != 2 or auth_response[1] != 0x00:
            raise AuthenticationError("SOCKS5 authentication failed")

    @staticmethod
    def build_connect_request(host: str, port: int) -> bytes:
        """Build SOCKS5 connection request."""
        request = bytearray([0x05, 0x01, 0x00])

        try:
            ip = ipaddress.ip_address(host)
            if isinstance(ip, ipaddress.IPv4Address):
                request.append(0x01)
                request.extend(ip.packed)
            else:
                request.append(0x04)
                request.extend(ip.packed)
        except ValueError:
            host_bytes = host.encode("utf-8")
            request.append(0x03)
            request.append(len(host_bytes))
            request.extend(host_bytes)

        request.extend(struct.pack(">H", port))
        return bytes(request)

    @staticmethod
    async def read_bound_address(reader: asyncio.StreamReader, addr_type: int) -> None:
        """Read bound address from SOCKS5 response."""
        if addr_type == 0x01:
            await reader.read(6)
        elif addr_type == 0x03:
            domain_len = (await reader.read(1))[0]
            await reader.read(domain_len + 2)
        elif addr_type == 0x04:
            await reader.read(18)

    @classmethod
    async def handshake(
        cls,
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        destination: Tuple[str, int],
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        """Perform complete SOCKS5 handshake."""
        host, port = destination

        # Authentication negotiation
        selected_method = await cls.negotiate_auth(
            writer, reader, username, password, timeout
        )

        # Handle authentication
        if selected_method == 0x02:
            if not username or not password:
                raise ConnectionError("SOCKS5 server requires authentication")
            await cls.authenticate(writer, reader, username, password, timeout)
        elif selected_method != 0x00:
            raise ConnectionError(f"Unsupported SOCKS5 auth method: {selected_method}")

        # Connection request
        request = cls.build_connect_request(host, port)
        writer.write(request)
        await writer.drain()

        # Read connection response
        conn_response = await asyncio.wait_for(reader.read(4), timeout)
        if (
            len(conn_response) != 4
            or conn_response[0] != 0x05
            or conn_response[1] != 0x00
        ):
            raise ConnectionError("SOCKS5 connection failed")

        # Read bound address
        await cls.read_bound_address(reader, conn_response[3])


class SOCKS4Handler:
    """Handles SOCKS4 proxy operations."""

    @staticmethod
    def build_request(host: str, port: int, username: Optional[str] = None) -> bytes:
        """Build SOCKS4 connection request."""
        try:
            ip = ipaddress.IPv4Address(host)
            ip_bytes = ip.packed
            user_id = (username or "pyrogram").encode("utf-8")
            request = (
                struct.pack(">BBH", 0x04, 0x01, port) + ip_bytes + user_id + b"\x00"
            )
        except ValueError:
            # SOCKS4A - use domain name
            ip_bytes = b"\x00\x00\x00\x01"
            user_id = (username or "pyrogram").encode("utf-8")
            request = (
                struct.pack(">BBH", 0x04, 0x01, port)
                + ip_bytes
                + user_id
                + b"\x00"
                + host.encode("utf-8")
                + b"\x00"
            )

        return request

    @classmethod
    async def handshake(
        cls,
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        destination: Tuple[str, int],
        *,
        username: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        """Perform SOCKS4 handshake."""
        host, port = destination
        request = cls.build_request(host, port, username)

        writer.write(request)
        await writer.drain()

        response = await asyncio.wait_for(reader.read(8), timeout)
        if len(response) != 8 or response[0] != 0x00 or response[1] != 0x5A:
            raise ConnectionError("SOCKS4 connection failed")


class HTTPProxyHandler:
    """Handles HTTP proxy operations."""

    @staticmethod
    def build_request(
        host: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        """Build HTTP CONNECT request."""
        request = f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n"

        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            request += f"Proxy-Authorization: Basic {credentials}\r\n"

        return request + "\r\n"

    @staticmethod
    def sanitize_request(request: str) -> str:
        """Sanitize HTTP request to prevent injection attacks."""
        if "\r\n\r\n" not in request:
            raise ValueError("Invalid HTTP request format")

        lines = request.split("\r\n")
        if not lines[0].startswith("CONNECT ") or "HTTP/1.1" not in lines[0]:
            raise ValueError("Invalid CONNECT request")

        return request

    @staticmethod
    async def read_response(reader: asyncio.StreamReader, timeout: int) -> list:
        """Read HTTP proxy response."""
        response_lines = []
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout)
            if not line:
                raise ConnectionError("HTTP proxy connection closed")

            line = line.decode("utf-8", errors="ignore").strip()
            response_lines.append(line)

            if not line:
                break

        return response_lines

    @classmethod
    async def handshake(
        cls,
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        destination: Tuple[str, int],
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        """Perform HTTP proxy handshake."""
        host, port = destination
        request = cls.build_request(host, port, username, password)
        sanitized_request = cls.sanitize_request(request)

        writer.write(sanitized_request.encode())
        await writer.drain()

        response_lines = await cls.read_response(reader, timeout)

        if not response_lines or not response_lines[0].startswith("HTTP/1."):
            raise ConnectionError("Invalid HTTP proxy response")

        status_parts = response_lines[0].split(" ", 2)
        if len(status_parts) < 2 or status_parts[1] != "200":
            raise ConnectionError(f"HTTP proxy connection failed: {response_lines[0]}")


class TCP:
    TIMEOUT = 10

    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        self.ipv6 = ipv6
        self.proxy = proxy

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

        self.lock = asyncio.Lock()

    def _get_proxy_handler(
        self, scheme: str
    ) -> Union[SOCKS5Handler, SOCKS4Handler, HTTPProxyHandler]:
        """Get appropriate proxy handler based on scheme."""
        handlers = {
            "SOCKS5": SOCKS5Handler,
            "SOCKS4": SOCKS4Handler,
            "HTTP": HTTPProxyHandler,
        }

        handler_class = handlers.get(scheme.upper())
        if not handler_class:
            raise ValueError(f"Unknown proxy type {scheme}")

        return handler_class

    def _validate_proxy_config(self) -> None:
        """Validate proxy configuration."""
        if not self.proxy.get("scheme"):
            raise ValueError("No scheme specified")

        if self.proxy["scheme"].upper() not in proxy_type_by_scheme:
            raise ValueError(f"Unknown proxy type {self.proxy['scheme']}")

    async def _establish_proxy_connection(
        self, hostname: str, port: int, proxy_family: int
    ) -> None:
        """Establish connection to proxy server."""
        self.reader, self.writer = await asyncio.wait_for(
            asyncio.open_connection(host=hostname, port=port, family=proxy_family),
            timeout=self.TIMEOUT,
        )

    def _get_proxy_family(self, hostname: str) -> int:
        """Determine address family for proxy connection."""
        try:
            ip_address = ipaddress.ip_address(hostname)
            return (
                socket.AF_INET6
                if isinstance(ip_address, ipaddress.IPv6Address)
                else socket.AF_INET
            )
        except ValueError:
            return socket.AF_INET

    async def _perform_handshake(
        self,
        scheme: str,
        destination: Tuple[str, int],
        username: Optional[str],
        password: Optional[str],
    ) -> None:
        """Perform proxy handshake based on scheme."""
        handler = self._get_proxy_handler(scheme)

        if scheme.upper() == "SOCKS5":
            await handler.handshake(
                self.writer,
                self.reader,
                destination,
                username=username,
                password=password,
                timeout=self.TIMEOUT,
            )
        elif scheme.upper() == "SOCKS4":
            await handler.handshake(
                self.writer,
                self.reader,
                destination,
                username=username,
            )
        elif scheme.upper() == "HTTP":
            await handler.handshake(
                self.writer,
                self.reader,
                destination,
                username=username,
                password=password,
                timeout=self.TIMEOUT,
            )

    async def _connect_via_proxy(self, destination: Tuple[str, int]) -> None:
        """Connect through proxy server."""
        self._validate_proxy_config()

        scheme = self.proxy["scheme"]
        hostname = self.proxy.get("hostname")
        port = self.proxy.get("port")
        username = self.proxy.get("username")
        password = self.proxy.get("password")

        proxy_family = self._get_proxy_family(hostname)

        try:
            await self._establish_proxy_connection(hostname, port, proxy_family)
            await self._perform_handshake(scheme, destination, username, password)
        except (ConnectionError, AuthenticationError, ValueError):
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
            raise
        except Exception as e:
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
            raise ConnectionError(f"Proxy connection failed: {e}") from e

    async def _connect_via_direct(self, destination: Tuple[str, int]) -> None:
        """Connect directly to destination."""
        host, port = destination
        family = socket.AF_INET6 if self.ipv6 else socket.AF_INET
        self.reader, self.writer = await asyncio.open_connection(
            host=host, port=port, family=family
        )

    async def _connect(self, destination: Tuple[str, int]) -> None:
        """Establish connection (direct or via proxy)."""
        if self.proxy:
            await self._connect_via_proxy(destination)
        else:
            await self._connect_via_direct(destination)

    async def connect(self, address: Tuple[str, int]) -> None:
        """Connect to the specified address."""
        try:
            await asyncio.wait_for(self._connect(address), self.TIMEOUT)
        except asyncio.TimeoutError:
            raise TimeoutError("Connection timed out")

    async def close(self) -> None:
        """Close the connection."""
        if self.writer is None:
            return None

        try:
            self.writer.close()
            await asyncio.wait_for(self.writer.wait_closed(), self.TIMEOUT)
        except (OSError, asyncio.TimeoutError):
            pass

    async def send(self, data: bytes) -> None:
        """Send data through the connection."""
        if self.writer is None:
            return None

        async with self.lock:
            try:
                self.writer.write(data)
                await self.writer.drain()
            except (OSError, asyncio.TimeoutError) as e:
                raise OSError(e)

    async def recv(self, length: int = 0) -> Optional[bytes]:
        """Receive data from the connection."""
        data = b""

        while len(data) < length:
            try:
                chunk = await asyncio.wait_for(
                    self.reader.read(length - len(data)), self.TIMEOUT
                )
            except (OSError, asyncio.TimeoutError):
                return None
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        return data
