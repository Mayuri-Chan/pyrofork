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
from inspect import iscoroutinefunction
from typing import Callable
import pyrofork

from pyrofork.types import Message, Identifier

from .handler import Handler


class MessageHandler(Handler):
    """The Message handler class. Used to handle new messages.
    It is intended to be used with :meth:`~pyrofork.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrofork.Client.on_message` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Message arrives. It takes *(client, message)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrofork.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        message (:obj:`~pyrofork.types.Message`):
            The received message.
    """

    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future_or_callback, filters)

    async def check_if_has_matching_listener(self, client: "pyrofork.Client", message: Message):
        """
        Checks if the message has a matching listener.

        :param client: The Client object to check with.
        :param message: The Message object to check with.
        :return: A tuple of whether the message has a matching listener and its filters does match with the Message
        and the matching listener;
        """
        from_user = message.from_user
        from_user_id = from_user.id if from_user else None
        from_user_username = from_user.username if from_user else None

        message_id = getattr(message, "id", getattr(message, "message_id", None))

        data = Identifier(
            message_id=message_id,
            chat_id=[message.chat.id, message.chat.username],
            from_user_id=[from_user_id, from_user_username],
        )

        listener = client.get_listener_matching_with_data(data, pyrofork.enums.ListenerTypes.MESSAGE)

        listener_does_match = False

        if listener:
            filters = listener.filters
            if callable(filters):
                if iscoroutinefunction(filters.__call__):
                    listener_does_match = await filters(client, message)
                else:
                    listener_does_match = await client.loop.run_in_executor(
                        None, filters, client, message
                    )
            else:
                listener_does_match = True

        return listener_does_match, listener

    async def check(self, client: "pyrofork.Client", message: Message):
        """
        Checks if the message has a matching listener or handler and its filters does match with the Message.

        :param client: Client object to check with.
        :param message: Message object to check with.
        :return: Whether the message has a matching listener or handler and its filters does match with the Message.
        """
        listener_does_match = (
            await self.check_if_has_matching_listener(client, message)
        )[0]

        if callable(self.filters):
            if iscoroutinefunction(self.filters.__call__):
                handler_does_match = await self.filters(client, message)
            else:
                handler_does_match = await client.loop.run_in_executor(
                    None, self.filters, client, message
                )
        else:
            handler_does_match = True

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    async def resolve_future_or_callback(self, client: "pyrofork.Client", message: Message, *args):
        """
        Resolves the future or calls the callback of the listener if the message has a matching listener.

        :param client: Client object to resolve or call with.
        :param message: Message object to resolve or call with.
        :param args: Arguments to call the callback with.
        :return: None
        """
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, message
        )

        if listener and listener_does_match:
            client.remove_listener(listener)

            if listener.future and not listener.future.done():
                listener.future.set_result(message)

                raise pyrofork.StopPropagation
            elif listener.callback:
                if iscoroutinefunction(listener.callback):
                    await listener.callback(client, message, *args)
                else:
                    listener.callback(client, message, *args)

                raise pyrofork.StopPropagation
            else:
                raise ValueError("Listener must have either a future or a callback")
        else:
            await self.original_callback(client, message, *args)