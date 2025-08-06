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
from typing import Tuple, Dict, TypedDict, Optional

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


class TCP:
    TIMEOUT = 10

    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        self.ipv6 = ipv6
        self.proxy = proxy

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

        self.lock = asyncio.Lock()

    async def _socks5_handshake(self, writer: asyncio.StreamWriter, reader: asyncio.StreamReader, 
                               destination: Tuple[str, int], username: Optional[str] = None, 
                               password: Optional[str] = None) -> None:
        # Authentication negotiation
        if username and password:
            auth_methods = b'\x05\x02\x00\x02'
        else:
            auth_methods = b'\x05\x01\x00'
        
        writer.write(auth_methods)
        await writer.drain()
        
        response = await asyncio.wait_for(reader.read(2), self.TIMEOUT)
        if len(response) != 2 or response[0] != 0x05:
            raise ConnectionError("Invalid SOCKS5 response")
        
        selected_method = response[1]
        
        # Authentication if required
        if selected_method == 0x02:
            if not username or not password:
                raise ConnectionError("SOCKS5 server requires authentication")
            
            username_bytes = username.encode('utf-8')
            password_bytes = password.encode('utf-8')
            auth_request = bytes([0x01, len(username_bytes)]) + username_bytes + bytes([len(password_bytes)]) + password_bytes
            
            writer.write(auth_request)
            await writer.drain()
            
            auth_response = await asyncio.wait_for(reader.read(2), self.TIMEOUT)
            if len(auth_response) != 2 or auth_response[1] != 0x00:
                raise ConnectionError("SOCKS5 authentication failed")
        
        elif selected_method != 0x00:
            raise ConnectionError(f"Unsupported SOCKS5 auth method: {selected_method}")
        
        # Connection request
        host, port = destination
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
            host_bytes = host.encode('utf-8')
            request.append(0x03)
            request.append(len(host_bytes))
            request.extend(host_bytes)
        
        request.extend(struct.pack('>H', port))
        
        writer.write(request)
        await writer.drain()
        
        conn_response = await asyncio.wait_for(reader.read(4), self.TIMEOUT)
        if len(conn_response) != 4 or conn_response[0] != 0x05 or conn_response[1] != 0x00:
            raise ConnectionError("SOCKS5 connection failed")
        
        # Read bound address
        addr_type = conn_response[3]
        if addr_type == 0x01:
            await reader.read(6)
        elif addr_type == 0x03:
            domain_len = (await reader.read(1))[0]
            await reader.read(domain_len + 2)
        elif addr_type == 0x04:
            await reader.read(18)

    async def _socks4_handshake(self, writer: asyncio.StreamWriter, reader: asyncio.StreamReader, 
                               destination: Tuple[str, int]) -> None:
        host, port = destination
        
        try:
            ip = ipaddress.IPv4Address(host)
            ip_bytes = ip.packed
        except ValueError:
            ip_bytes = b'\x00\x00\x00\x01'
        
        request = struct.pack('>BBH', 0x04, 0x01, port) + ip_bytes + b'pyrogram\x00'
        
        if ip_bytes == b'\x00\x00\x00\x01':
            request += host.encode('utf-8') + b'\x00'
        
        writer.write(request)
        await writer.drain()
        
        response = await asyncio.wait_for(reader.read(8), self.TIMEOUT)
        if len(response) != 8 or response[0] != 0x00 or response[1] != 0x5A:
            raise ConnectionError("SOCKS4 connection failed")

    async def _http_proxy_handshake(self, writer: asyncio.StreamWriter, reader: asyncio.StreamReader,
                                   destination: Tuple[str, int], username: Optional[str] = None,
                                   password: Optional[str] = None) -> None:
        host, port = destination
        
        request = f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n"
        
        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            request += f"Proxy-Authorization: Basic {credentials}\r\n"
        
        request += "\r\n"
        
        writer.write(request.encode())
        await writer.drain()
        
        response_lines = []
        while True:
            line = await asyncio.wait_for(reader.readline(), self.TIMEOUT)
            if not line:
                raise ConnectionError("HTTP proxy connection closed")
            
            line = line.decode('utf-8', errors='ignore').strip()
            response_lines.append(line)
            
            if not line:
                break
        
        if not response_lines or not response_lines[0].startswith('HTTP/1.'):
            raise ConnectionError("Invalid HTTP proxy response")
        
        status_parts = response_lines[0].split(' ', 2)
        if len(status_parts) < 2 or status_parts[1] != '200':
            raise ConnectionError(f"HTTP proxy connection failed: {response_lines[0]}")

    async def _connect_via_proxy(self, destination: Tuple[str, int]) -> None:
        scheme = self.proxy.get("scheme")
        if scheme is None:
            raise ValueError("No scheme specified")

        proxy_type = proxy_type_by_scheme.get(scheme.upper())
        if proxy_type is None:
            raise ValueError(f"Unknown proxy type {scheme}")

        hostname = self.proxy.get("hostname")
        port = self.proxy.get("port")
        username = self.proxy.get("username")
        password = self.proxy.get("password")

        try:
            ip_address = ipaddress.ip_address(hostname)
        except ValueError:
            is_proxy_ipv6 = False
        else:
            is_proxy_ipv6 = isinstance(ip_address, ipaddress.IPv6Address)

        proxy_family = socket.AF_INET6 if is_proxy_ipv6 else socket.AF_INET
        
        try:
            # Connect to proxy server
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(
                    host=hostname,
                    port=port,
                    family=proxy_family
                ),
                timeout=self.TIMEOUT
            )
            
            # Perform proxy handshake
            if proxy_type == socks.SOCKS5:
                await self._socks5_handshake(self.writer, self.reader, destination, username, password)
            elif proxy_type == socks.SOCKS4:
                await self._socks4_handshake(self.writer, self.reader, destination)
            elif proxy_type == socks.HTTP:
                await self._http_proxy_handshake(self.writer, self.reader, destination, username, password)
            else:
                raise ValueError(f"Unsupported proxy type: {scheme}")
            
        except Exception:
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
            raise

    async def _connect_via_direct(self, destination: Tuple[str, int]) -> None:
        host, port = destination
        family = socket.AF_INET6 if self.ipv6 else socket.AF_INET
        self.reader, self.writer = await asyncio.open_connection(
            host=host,
            port=port,
            family=family
        )

    async def _connect(self, destination: Tuple[str, int]) -> None:
        if self.proxy:
            await self._connect_via_proxy(destination)
        else:
            await self._connect_via_direct(destination)

    async def connect(self, address: Tuple[str, int]) -> None:
        try:
            await asyncio.wait_for(self._connect(address), self.TIMEOUT)
        except asyncio.TimeoutError:
            raise TimeoutError("Connection timed out")

    async def close(self) -> None:
        if self.writer is None:
            return None

        try:
            self.writer.close()
            await asyncio.wait_for(self.writer.wait_closed(), self.TIMEOUT)
        except Exception:
            pass

    async def send(self, data: bytes) -> None:
        if self.writer is None:
            return None

        async with self.lock:
            try:
                self.writer.write(data)
                await self.writer.drain()
            except Exception as e:
                raise OSError(e)

    async def recv(self, length: int = 0) -> Optional[bytes]:
        data = b""

        while len(data) < length:
            try:
                chunk = await asyncio.wait_for(
                    self.reader.read(length - len(data)),
                    self.TIMEOUT
                )
            except (OSError, asyncio.TimeoutError):
                return None
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        return data