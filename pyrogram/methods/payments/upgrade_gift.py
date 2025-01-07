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
from pyrogram import raw, errors


class UpgradeGift:
    async def upgrade_gift(
        self: "pyrogram.Client",
        message_id: int,
        keep_details: Optional[bool] = None
    ) -> bool:
        """Upgrade star gift to unique.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            message_id (``int``):
                Unique message identifier of star gift.

            keep_details (``bool``):
                Pass True if you want to keep the original details of the gift like caption.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Upgrade gift
                app.upgrade_gift(message_id=123)
        """
        try:
            await self.invoke(
                raw.functions.payments.UpgradeStarGift(
                    msg_id=message_id,
                    keep_original_details=keep_details
                )
            )
        except errors.PaymentRequired:
            invoice = raw.types.InputInvoiceStarGiftUpgrade(
                msg_id=message_id,
                keep_original_details=keep_details
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
