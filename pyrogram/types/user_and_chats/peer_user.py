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


from pyrogram import raw
from ..object import Object


class PeerUser(Object):
    """A PeerUser.


    Parameters:
        user_id (``Integer``):
            Id of the user.
    """

    def __init__(
        self, *,
        user_id: int
    ):
        super().__init__()

        self.user_id = user_id

    @staticmethod
    def _parse(action: "raw.types.PeerUser") -> "PeerUser":


        return PeerUser(
            user_id=getattr(action,"user_id", None)
        )
