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

from uuid import uuid4

import pyrofork
from pyrofork import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~pyrofork.types.InlineQueryResultCachedAudio`
    - :obj:`~pyrofork.types.InlineQueryResultCachedDocument`
    - :obj:`~pyrofork.types.InlineQueryResultCachedAnimation`
    - :obj:`~pyrofork.types.InlineQueryResultCachedPhoto`
    - :obj:`~pyrofork.types.InlineQueryResultCachedSticker`
    - :obj:`~pyrofork.types.InlineQueryResultCachedVideo`
    - :obj:`~pyrofork.types.InlineQueryResultCachedVoice`
    - :obj:`~pyrofork.types.InlineQueryResultArticle`
    - :obj:`~pyrofork.types.InlineQueryResultAudio`
    - :obj:`~pyrofork.types.InlineQueryResultContact`
    - :obj:`~pyrofork.types.InlineQueryResultDocument`
    - :obj:`~pyrofork.types.InlineQueryResultAnimation`
    - :obj:`~pyrofork.types.InlineQueryResultLocation`
    - :obj:`~pyrofork.types.InlineQueryResultPhoto`
    - :obj:`~pyrofork.types.InlineQueryResultVenue`
    - :obj:`~pyrofork.types.InlineQueryResultVideo`
    - :obj:`~pyrofork.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "pyrofork.Client"):
        pass
