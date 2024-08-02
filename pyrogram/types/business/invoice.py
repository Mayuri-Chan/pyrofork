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

import pyrogram

from pyrogram import raw, types, utils
from ..object import Object


class Invoice(Object):
    """Contains information about an Invoice.

    Parameters:
        title (``str``):
            Product name.

        description (``str``):
            Product description.

        currency (``str``):
            Currency code.

        total_amount (``int``):
            Total price in the smallest units of the currency.

        start_parameter (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice.

        shipping_address_requested (``bool``, *optional*):
            True, if the the shipping address is requested.

        test (``bool``, *optional*):
            True, if the invoice is a test invoice.

        receipt_message_id (``int``, *optional*):
            The message_id of the message sent to the chat when the invoice is paid.
    """

    def __init__(
        self,
        *,
        title: str,
        description :  str,
        currency: str,
        total_amount: int,
        start_parameter: str,
        shipping_address_requested: bool = None,
        test: bool = None,
        receipt_message_id: int = None,
        # TODO: Implement photo, extended_media parameters
    ):
        super().__init__()

        self.title = title
        self.description = description
        self.currency = currency
        self.total_amount = total_amount
        self.start_parameter = start_parameter
        self.shipping_address_requested = shipping_address_requested
        self.test = test
        self.receipt_message_id = receipt_message_id

    @staticmethod
    def _parse(
        message_invoice: "raw.types.MessageMediaInvoice"
    ) -> "Invoice":
        return Invoice(
            title=message_invoice.title,
            description=message_invoice.description,
            currency=message_invoice.currency,
            total_amount=message_invoice.total_amount,
            start_parameter=message_invoice.start_param,
            shipping_address_requested=message_invoice.shipping_address_requested,
            test=message_invoice.test,
            receipt_message_id=message_invoice.receipt_msg_id
        )
