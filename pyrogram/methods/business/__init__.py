#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
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
from .answer_shipping_query import AnswerShippingQuery
from .delete_business_messages import DeleteBusinessMessages
from .get_business_connection import GetBusinessConnection
from .get_business_account_gifts import GetBusinessAccountGifts
from .get_business_account_star_balance import GetBusinessAccountStarBalance
from .transfer_business_account_stars import TransferBusinessAccountStars


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    DeleteBusinessMessages,
    GetBusinessConnection,
    GetBusinessAccountGifts,
    GetBusinessAccountStarBalance,
    TransferBusinessAccountStars,
):
    pass
