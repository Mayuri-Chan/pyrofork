#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import errors, raw


class TransferGift:
    async def transfer_gift(
        self: "pyrogram.Client",
        message_id: int,
        to_chat_id: Union[int, str],
    ) -> bool:
        """Transfer star gift to another user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            message_id (``int``):
                Unique message identifier of star gift.

            to_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat you want to transfer the star gift to.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Transfer gift to another user
                app.transfer_gift(message_id=123, to_chat_id=123)
        """
        peer = await self.resolve_peer(to_chat_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("chat_id must belong to a user.")

        try:
            await self.invoke(
                raw.functions.payments.TransferStarGift(
                    stargift=raw.types.InputSavedStarGiftUser(
                        msg_id=message_id
                    ),
                    to_id=peer
                )
            )
        except errors.PaymentRequired:
            invoice = raw.types.InputInvoiceStarGiftTransfer(
                stargift=raw.types.InputSavedStarGiftUser(
                    msg_id=message_id
                ),
                to_id=peer
            )

            form = await self.invoke(
                raw.functions.payments.GetPaymentForm(
                    invoice=invoice
                )
            )

            await self.invoke(
                raw.functions.payments.SendStarsForm(
                    form_id=form.form_id,
                    invoice=invoice
                )
            )

        return True
