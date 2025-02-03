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

from .apply_gift_code import ApplyGiftCode
from .check_giftcode import CheckGiftCode
from .convert_gift import ConvertGift
from .create_invoice_link import CreateInvoiceLink
from .get_payment_form import GetPaymentForm
from .get_stars_balance import GetStarsBalance
from .get_upgraded_gift import GetUpgradedGift
from .get_available_gifts import GetAvailableGifts
from .get_stars_transactions import GetStarsTransactions
from .get_stars_transactions_by_id import GetStarsTransactionsById
from .get_chat_gifts_count import GetChatGiftsCount
from .get_chat_gifts import GetChatGifts
from .hide_gift import HideGift
from .refund_stars_payment import RefundStarPayment
from .send_invoice import SendInvoice
from .send_paid_media import SendPaidMedia
from .send_paid_reaction import SendPaidReaction
from .send_payment_form import SendPaymentForm
from .send_gift import SendGift
from .show_gift import ShowGift
from .transfer_gift import TransferGift
from .upgrade_gift import UpgradeGift

class Payments(
    ApplyGiftCode,
    CheckGiftCode,
    ConvertGift,
    CreateInvoiceLink,
    GetPaymentForm,
    GetStarsBalance,
    GetUpgradedGift,
    GetAvailableGifts,
    GetStarsTransactions,
    GetStarsTransactionsById,
    GetChatGiftsCount,
    GetChatGifts,
    HideGift,
    RefundStarPayment,
    SendPaidReaction,
    SendPaidMedia,
    SendInvoice,
    SendPaymentForm,
    SendGift,
    ShowGift,
    TransferGift,
    UpgradeGift
):
    pass
