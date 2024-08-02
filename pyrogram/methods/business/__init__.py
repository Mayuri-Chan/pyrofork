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

from .answer_pre_checkout_query import AnswerPreCheckoutQuery
from .create_invoice_link import CreateInvoiceLink
from .get_business_connection import GetBusinessConnection
from .get_stars_transactions import GetStarsTransactions
from .get_stars_transactions_by_id import GetStarsTransactionsById
from .refund_stars_payment import RefundStarPayment
from .send_invoice import SendInvoice
from .send_paid_media import SendPaidMedia


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    CreateInvoiceLink,
    GetBusinessConnection,
    GetStarsTransactions,
    GetStarsTransactionsById,
    RefundStarPayment,
    SendInvoice,
    SendPaidMedia
):
    pass
