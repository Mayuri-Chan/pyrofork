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

import re
from typing import Union

import pyrogram
from pyrogram import raw, types


class GetPaymentForm:
    async def get_payment_form(
        self: "pyrogram.Client", *,
        chat_id: Union[int, str] = None,
        message_id: int = None,
        invoice_link: str = None
    ) -> "types.PaymentForm":
        """Get information about a invoice or paid media.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                of the target channel/supergroup (in the format @username).

            message_id (``int``):
                Pass a message identifier or to get the invoice from message.

            invoice_link (``str``):
                Pass a invoice link in form of a *t.me/$...* link or slug itself to get the payment form from link.

        Returns:
            :obj:`~pyrogram.types.PaymentForm`: On success, a payment form is returned.

        Example:
            .. code-block:: python

                # get payment form from message
                app.get_payment_form(chat_id=chat_id, message_id=123)

                # get payment form from link
                app.get_payment_form(invoice_link="https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk")
        """
        if not any((all((chat_id, message_id)), invoice_link)):
            raise ValueError("You should pass at least one parameter to this method.")

        invoice = None

        if message_id:
            invoice = raw.types.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        elif invoice_link:
            match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/\$)([\w-]+)$", invoice_link)

            if match:
                slug = match.group(1)
            else:
                slug = invoice_link

            invoice = raw.types.InputInvoiceSlug(
                slug=slug
            )

        r = await self.invoke(
            raw.functions.payments.GetPaymentForm(
                invoice=invoice
            )
        )

        return types.PaymentForm._parse(self, r)
