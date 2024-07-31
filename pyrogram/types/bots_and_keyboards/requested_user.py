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

from ..object import Object
from pyrogram import enums, raw, types
from typing import Union

class RequestedUser(Object):
    """Contains information about a requested user.

    Parameters:
        user_id (``int``):
            Identifier of the user.

        first_name (``str``, *optional*):
            First name of the user.

        last_name (``str``, *optional*):
            Last name of the user.

        username (``str``, *optional*):
            Username of the user.

        photo (``types.UserProfilePhoto``, *optional*):
            User photo.

        full_name (``str``, *optional*):
            User's full name.
    """
    def __init__(
        self,
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        username: str = None,
        photo: "types.ChatPhoto" = None,
    ):
        super().__init__()

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.photo = photo

    @staticmethod
    async def _parse(
        client,
        request: Union[
            "raw.types.RequestedPeerUser",
            "raw.types.PeerUser"
        ]
    ) -> "RequestedUser":

        photo = None
        if getattr(request,"photo", None):
            photo = types.Photo._parse(client, getattr(request,"photo", None), 0)

        return RequestedUser(
            user_id=getattr(request,"user_id", None),
            first_name=getattr(request,"first_name", None),
            last_name=getattr(request,"last_name", None),
            username=getattr(request,"username", None),
            photo=photo
        )

    @property
    def full_name(self) -> str:
        return " ".join(filter(None, [self.first_name, self.last_name])) or None
