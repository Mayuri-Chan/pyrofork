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

from ..object import Object


class PaymentInfo(Object):
    """Contains information about a payment.

    Parameters:
        name (``str``, *optional*):
            User's name.

        phone_number (``str``, *optional*):
            User's phone number.

        email (``str``, *optional*):
            User's email.

        shipping_address (:obj:`~pyrogram.types.ShippingAddress`, *optional*):
            User's shipping address.
    """

    def __init__(
        self, *,
        name: str = None,
        phone_number: str = None,
        email: str = None,
        shipping_address: "types.ShippingAddress" = None
    ):
        super().__init__()

        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address
