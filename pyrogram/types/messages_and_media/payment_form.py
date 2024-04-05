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

from typing import Optional

import pyrogram
from pyrogram import types, raw
from ..object import Object


class PaymentForm(Object):
    """This object contains basic information about an payment form.

    Parameters:
        id (``int``):
            Form id.

        bot (``str``):
            Bot.

        title (``str``):
            Form title.

        description (``str``):
            Form description.

        invoice (``str``):
            Invoice.

        provider (``str``, *optional*):
            Payment provider.

        url (``str``, *optional*):
            Payment form URL.

        can_save_credentials (``str``, *optional*):
            Whether the user can choose to save credentials.

        is_password_missing (``str``, *optional*):
            Indicates that the user can save payment credentials,
            but only after setting up a 2FA password
            (currently the account doesn't have a 2FA password).

        native_provider (``str``, *optional*):
            Payment provider name.

        raw (:obj:`~raw.base.payments.PaymentForm`, *optional*):
            The raw object, as received from the Telegram API.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        bot: "types.User",
        title: str,
        description: str,
        invoice: "types.Invoice",
        provider: Optional["types.User"] = None,
        url: Optional[str] = None,
        can_save_credentials: Optional[bool] = None,
        is_password_missing: Optional[bool] = None,
        native_provider: Optional[str] = None,
        raw: "raw.base.payments.PaymentForm" = None,
        # TODO: Add support for other params:
        # native_params
        # additional_params
        # saved_info
        # saved_credentials
    ):
        super().__init__(client)

        self.id = id
        self.bot = bot
        self.title = title
        self.description = description
        self.invoice = invoice
        self.provider = provider
        self.url = url
        self.can_save_credentials = can_save_credentials
        self.is_password_missing = is_password_missing
        self.native_provider = native_provider
        self.raw = raw

    @staticmethod
    def _parse(client, payment_form: "raw.base.payments.PaymentForm") -> "PaymentForm":
        users = {i.id: i for i in payment_form.users}

        return PaymentForm(
            id=payment_form.form_id,
            bot=types.User._parse(client, users.get(payment_form.bot_id)),
            title=payment_form.title,
            description=payment_form.description,
            invoice=types.Invoice._parse(client, payment_form.invoice),
            provider=types.User._parse(client, users.get(getattr(payment_form, "provider_id", None))),
            url=getattr(payment_form, "url", None),
            can_save_credentials=getattr(payment_form, "can_save_credentials", None),
            is_password_missing=getattr(payment_form, "password_missing", None),
            native_provider=getattr(payment_form, "native_provider", None),
            raw=payment_form
        )
