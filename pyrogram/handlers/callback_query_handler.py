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

from typing import Callable, Tuple

import pyrogram

from pyrogram.utils import PyromodConfig
from pyrogram.types import ListenerTypes, CallbackQuery, Identifier, Listener

from .handler import Handler


class CallbackQueryHandler(Handler):
    """The CallbackQuery handler class. Used to handle callback queries coming from inline buttons.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_callback_query` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new CallbackQuery arrives. It takes *(client, callback_query)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of callback queries to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        callback_query (:obj:`~pyrogram.types.CallbackQuery`):
            The received callback query.
    """

    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future, filters)

    def compose_data_identifier(self, query: CallbackQuery):
        from_user = query.from_user
        from_user_id = from_user.id if from_user else None

        chat_id = None
        message_id = None

        if query.message:
            message_id = getattr(
                query.message, "id", getattr(query.message, "message_id", None)
            )

            if query.message.chat:
                chat_id = query.message.chat.id

        return Identifier(
            message_id=message_id,
            chat_id=chat_id,
            from_user_id=from_user_id,
            inline_message_id=query.inline_message_id,
        )

    async def check_if_has_matching_listener(
        self, client: "pyrogram.Client", query: CallbackQuery
    ) -> Tuple[bool, Listener]:
        data = self.compose_data_identifier(query)

        listener = client.get_matching_listener(data, ListenerTypes.CALLBACK_QUERY)

        listener_does_match = False

        if listener:
            filters = listener.filters
            listener_does_match = (
                await filters(client, query) if callable(filters) else True
            )

        return listener_does_match, listener

    async def check(self, client: "pyrogram.Client", query: CallbackQuery):
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, query
        )

        handler_does_match = (
            await self.filters(client, query) if callable(self.filters) else True
        )

        data = self.compose_data_identifier(query)

        if PyromodConfig.unallowed_click_alert:
            # matches with the current query but from any user
            permissive_identifier = Identifier(
                chat_id=data.chat_id,
                message_id=data.message_id,
                inline_message_id=data.inline_message_id,
                from_user_id=None,
            )

            matches = permissive_identifier.matches(data)

            if (
                listener
                and (matches and not listener_does_match)
                and listener.unallowed_click_alert
            ):
                alert = (
                    listener.unallowed_click_alert
                    if isinstance(listener.unallowed_click_alert, str)
                    else PyromodConfig.unallowed_click_alert_text
                )
                await query.answer(alert)
                return False

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    async def resolve_future(self, client: "pyrogram.Client", query: CallbackQuery, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, query
        )

        if listener and not listener.future.done():
            listener.future.set_result(query)
            client.remove_listener(listener)
            raise pyrogram.StopPropagation
        else:
            await self.original_callback(client, query, *args)
