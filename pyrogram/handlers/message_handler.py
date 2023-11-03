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

from typing import Callable
import pyrogram

from pyrogram.types import ListenerTypes, Message, Identifier

from .handler import Handler


class MessageHandler(Handler):
    """The Message handler class. Used to handle new messages.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_message` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Message arrives. It takes *(client, message)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        message (:obj:`~pyrogram.types.Message`):
            The received message.
    """

    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future, filters)

    async def check_if_has_matching_listener(self, client: "pyrogram.Client", message: Message):
        from_user = message.from_user
        from_user_id = from_user.id if from_user else None

        message_id = getattr(message, "id", getattr(message, "message_id", None))

        data = Identifier(
            message_id=message_id, chat_id=message.chat.id, from_user_id=from_user_id
        )

        listener = client.get_matching_listener(data, ListenerTypes.MESSAGE)

        listener_does_match = False

        if listener:
            filters = listener.filters
            listener_does_match = (
                await filters(client, message) if callable(filters) else True
            )

        return listener_does_match, listener

    async def check(self, client: "pyrogram.Client", message: Message):
        listener_does_match = (
            await self.check_if_has_matching_listener(client, message)
        )[0]

        handler_does_match = (
            await self.filters(client, message) if callable(self.filters) else True
        )

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    async def resolve_future(self, client: "pyrogram.Client", message: Message, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, message
        )

        if listener_does_match:
            if not listener.future.done():
                listener.future.set_result(message)
                client.remove_listener(listener)
                raise pyrogram.StopPropagation
        else:
            await self.original_callback(client, message, *args)