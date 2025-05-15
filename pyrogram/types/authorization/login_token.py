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

from pyrogram import raw


class LoginToken(Object):
    """Contains info on a login token.

    Parameters:
        token (``str``):
            The login token.

        expires (``int``):
            The expiration date of the token in UNIX format.
    """

    def __init__(self, *, token: str, expires: int):
        super().__init__()

        self.token = token
        self.expires = expires

    @staticmethod
    def _parse(login_token: "raw.base.LoginToken") -> "LoginToken":
        return LoginToken(
            token=login_token.token,
            expires=login_token.expires,
        )
