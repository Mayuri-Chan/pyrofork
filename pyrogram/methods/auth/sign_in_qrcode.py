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
from base64 import b64encode
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.session import Session, Auth

log = logging.getLogger(__name__)

QRCODE_AVAIL = False
try:
    import qrcode
    QRCODE_AVAIL = True
except ImportError:
    QRCODE_AVAIL = False


class SignInQrcode:
    async def sign_in_qrcode(
        self: "pyrogram.Client"
    ) -> Union["types.User", "types.LoginToken"]:
        """Authorize a user in Telegram with a QR code.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            :obj:`~pyrogram.types.User` | :obj:`pyrogram.types.LoginToken`, in case the
            authorization completed, the user is returned. In case the QR code is
            not scanned, a login token is returned.

        Raises:
            ImportError: In case the qrcode library is not installed.
            SessionPasswordNeeded: In case a password is needed to sign in.
        """

        if not QRCODE_AVAIL:
            raise ImportError("qrcode is missing! "
                            "Please install it with `pip install qrcode`")
        r = await self.session.invoke(
            raw.functions.auth.ExportLoginToken(
                api_id=self.api_id,
                api_hash=self.api_hash,
                except_ids=[]
            )
        )
        if isinstance(r, raw.types.auth.LoginToken):
            base64_token = b64encode(r.token).decode("utf-8")
            login_url = f"tg://login?token={base64_token}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(login_url)
            qr.make(fit=True)

            print("Scan the QR code with your Telegram app.")
            qr.print_ascii()

            return r
        elif isinstance(r, raw.types.auth.LoginTokenSuccess):
            await self.storage.user_id(r.authorization.user.id)
            await self.storage.is_bot(False)

            return types.User._parse(self, r.authorization.user)
        elif isinstance(r, raw.types.auth.LoginTokenMigrateTo):
            # pylint: disable=access-member-before-definition
            await self.session.stop()

            await self.storage.dc_id(r.dc_id)
            await self.storage.auth_key(
                await Auth(
                    self, await self.storage.dc_id(),
                    await self.storage.test_mode()
                ).create()
            )
            self.session = Session(
                self, await self.storage.dc_id(),
                await self.storage.auth_key(), await self.storage.test_mode()
            )

            await self.session.start()
            r = await self.session.invoke(
                raw.functions.auth.ImportLoginToken(
                    token=r.token
                )
            )
            if isinstance(r, raw.types.auth.LoginToken):
                base64_token = b64encode(r.token).decode("utf-8")
                login_url = f"tg://login?token={base64_token}"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(login_url)
                qr.make(fit=True)

                print("Scan the QR code below with your Telegram app.")
                qr.print_ascii()

                return types.LoginToken(
                    self,
                    r.token,
                    r.expires
                )
            elif isinstance(r, raw.types.auth.LoginTokenSuccess):
                await self.storage.user_id(r.authorization.user.id)
                await self.storage.is_bot(False)

                return types.User._parse(self, r.authorization.user)
        else:
            raise pyrogram.exceptions.RPCError(
                "Unknown response type from Telegram API"
            )
        return r
