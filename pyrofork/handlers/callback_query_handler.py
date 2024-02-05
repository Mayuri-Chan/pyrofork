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

from asyncio import iscoroutinefunction
from typing import Callable, Tuple

import pyrofork

from pyrofork.utils import PyromodConfig
from pyrofork.types import CallbackQuery, Identifier, Listener

from .handler import Handler


class CallbackQueryHandler(Handler):
    """The CallbackQuery handler class. Used to handle callback queries coming from inline buttons.
    It is intended to be used with :meth:`~pyrofork.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrofork.Client.on_callback_query` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new CallbackQuery arrives. It takes *(client, callback_query)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of callback queries to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrofork.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        callback_query (:obj:`~pyrofork.types.CallbackQuery`):
            The received callback query.
    """

    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future_or_callback, filters)

    def compose_data_identifier(self, query: CallbackQuery):
        """
        Composes an Identifier object from a CallbackQuery object.

        :param query: The CallbackQuery object to compose of.
        :return: An Identifier object.
        """
        from_user = query.from_user
        from_user_id = from_user.id if from_user else None
        from_user_username = from_user.username if from_user else None

        chat_id = None
        message_id = None

        if query.message:
            message_id = getattr(
                query.message, "id", getattr(query.message, "message_id", None)
            )

            if query.message.chat:
                chat_id = [query.message.chat.id, query.message.chat.username]

        return Identifier(
            message_id=message_id,
            chat_id=chat_id,
            from_user_id=[from_user_id, from_user_username],
            inline_message_id=query.inline_message_id,
        )

    async def check_if_has_matching_listener(
        self, client: "pyrofork.Client", query: CallbackQuery
    ) -> Tuple[bool, Listener]:
        """
        Checks if the CallbackQuery object has a matching listener.

        :param client: The Client object to check with.
        :param query: The CallbackQuery object to check with.
        :return: A tuple of a boolean and a Listener object. The boolean indicates whether
        the found listener has filters and its filters matches with the CallbackQuery object.
        The Listener object is the matching listener.
        """
        data = self.compose_data_identifier(query)

        listener = client.get_listener_matching_with_data(
            data, pyrofork.enums.ListenerTypes.CALLBACK_QUERY
        )

        listener_does_match = False

        if listener:
            filters = listener.filters
            if callable(filters):
                if iscoroutinefunction(filters.__call__):
                    listener_does_match = await filters(client, query)
                else:
                    listener_does_match = await client.loop.run_in_executor(
                        None, filters, client, query
                    )
            else:
                listener_does_match = True

        return listener_does_match, listener

    async def check(self, client: "pyrofork.Client", query: CallbackQuery):
        """
        Checks if the CallbackQuery object has a matching listener or handler.

        :param client: The Client object to check with.
        :param query: The CallbackQuery object to check with.
        :return: A boolean indicating whether the CallbackQuery object has a matching listener or the handler
        filter matches.
        """
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, query
        )

        if callable(self.filters):
            if iscoroutinefunction(self.filters.__call__):
                handler_does_match = await self.filters(client, query)
            else:
                handler_does_match = await client.loop.run_in_executor(
                    None, self.filters, client, query
                )
        else:
            handler_does_match = True

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

    async def resolve_future_or_callback(
        self, client: "pyrofork.Client", query: CallbackQuery, *args
    ):
        """
        Resolves the future or calls the callback of the listener. Will call the original handler if no listener.

        :param client: The Client object to resolve or call with.
        :param query: The CallbackQuery object to resolve or call with.
        :param args: The arguments to call the callback with.
        :return: None
        """
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, query
        )

        if listener and listener_does_match:
            client.remove_listener(listener)

            if listener.future and not listener.future.done():
                listener.future.set_result(query)

                raise pyrofork.StopPropagation
            elif listener.callback:
                if iscoroutinefunction(listener.callback):
                    await listener.callback(client, query, *args)
                else:
                    listener.callback(client, query, *args)

                raise pyrofork.StopPropagation
            else:
                raise ValueError("Listener must have either a future or a callback")
        else:
            await self.original_callback(client, query, *args)
