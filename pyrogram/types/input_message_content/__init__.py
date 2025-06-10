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

from .input_message_content import InputMessageContent
from .input_reply_to_message import InputReplyToMessage
from .input_reply_to_monoforum import InputReplyToMonoforum
from .input_reply_to_story import InputReplyToStory
from .input_text_message_content import InputTextMessageContent
from .input_location_message_content import InputLocationMessageContent
from .input_venue_message_content import InputVenueMessageContent
from .input_contact_message_content import InputContactMessageContent
from .input_invoice_message_content import InputInvoiceMessageContent

__all__ = [
    "InputMessageContent",
    "InputReplyToMessage",
    "InputReplyToMonoforum",
    "InputReplyToStory",
    "InputTextMessageContent",
    "InputLocationMessageContent",
    "InputVenueMessageContent",
    "InputContactMessageContent",
    "InputInvoiceMessageContent"
]
