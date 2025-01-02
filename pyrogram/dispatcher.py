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

import asyncio
import inspect
import logging
from collections import OrderedDict

import pyrogram
from pyrogram import errors, raw, types, utils
from pyrogram.handlers.handler import Handler
from pyrogram.handlers import (
  BotBusinessConnectHandler,
  BotBusinessMessageHandler,
  CallbackQueryHandler,
  MessageHandler,
  EditedMessageHandler,
  EditedBotBusinessMessageHandler,
  ErrorHandler,
  DeletedMessagesHandler,
  DeletedBotBusinessMessagesHandler,
  MessageReactionUpdatedHandler,
  MessageReactionCountUpdatedHandler,
  UserStatusHandler,
  RawUpdateHandler,
  InlineQueryHandler,
  PollHandler,
  ShippingQueryHandler,
  PreCheckoutQueryHandler,
  ConversationHandler,
  ChosenInlineResultHandler,
  ChatMemberUpdatedHandler,
  ChatJoinRequestHandler,
  StoryHandler,
  PurchasedPaidMediaHandler
)
from pyrogram.raw.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateBotBusinessConnect,
    UpdateBotNewBusinessMessage, UpdateBotDeleteBusinessMessage, UpdateBotEditBusinessMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery, UpdateBotPrecheckoutQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll,
    UpdateBotInlineSend, UpdateChatParticipant, UpdateChannelParticipant, UpdateBotStopped,
    UpdateBotChatInviteRequester, UpdateStory,
    UpdateBotMessageReaction,
    UpdateBotMessageReactions,
    UpdateBotShippingQuery,
    UpdateBusinessBotCallbackQuery,
    UpdateBotPurchasedPaidMedia
)

log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage)
    NEW_BOT_BUSINESS_MESSAGE_UPDATES = (UpdateBotNewBusinessMessage,)
    EDIT_MESSAGE_UPDATES = (UpdateEditMessage, UpdateEditChannelMessage)
    EDIT_BOT_BUSINESS_MESSAGE_UPDATES = (UpdateBotEditBusinessMessage,)
    DELETE_MESSAGES_UPDATES = (UpdateDeleteMessages, UpdateDeleteChannelMessages)
    DELETE_BOT_BUSINESS_MESSAGES_UPDATES = (UpdateBotDeleteBusinessMessage,)
    CALLBACK_QUERY_UPDATES = (UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery, UpdateBusinessBotCallbackQuery)
    CHAT_MEMBER_UPDATES = (UpdateChatParticipant, UpdateChannelParticipant, UpdateBotStopped,)
    USER_STATUS_UPDATES = (UpdateUserStatus,)
    BOT_INLINE_QUERY_UPDATES = (UpdateBotInlineQuery,)
    POLL_UPDATES = (UpdateMessagePoll,)
    CHOSEN_INLINE_RESULT_UPDATES = (UpdateBotInlineSend,)
    CHAT_JOIN_REQUEST_UPDATES = (UpdateBotChatInviteRequester,)
    NEW_STORY_UPDATES = (UpdateStory,)
    MESSAGE_BOT_NA_REACTION_UPDATES = (UpdateBotMessageReaction,)
    MESSAGE_BOT_A_REACTION_UPDATES = (UpdateBotMessageReactions,)
    BOT_BUSSINESS_CONNECT_UPDATES = (UpdateBotBusinessConnect,)
    PRE_CHECKOUT_QUERY_UPDATES = (UpdateBotPrecheckoutQuery,)
    SHIPPING_QUERY_UPDATES = (UpdateBotShippingQuery,)
    PURCHASED_PAID_MEDIA_UPDATES = (UpdateBotPurchasedPaidMedia,)

    def __init__(self, client: "pyrogram.Client"):
        self.client = client
        self.loop = asyncio.get_event_loop()

        self.handler_worker_tasks = []
        self.locks_list = []
        self.error_handlers = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        self.conversation_handler = ConversationHandler()
        self.groups[0] = [self.conversation_handler]

        async def message_parser(update, users, chats):
            return (
                await pyrogram.types.Message._parse(self.client, update.message, users, chats,
                                                    is_scheduled=isinstance(update, UpdateNewScheduledMessage)),
                MessageHandler
            )

        async def bot_business_message_parser(update, users, chats):
            return (
                await pyrogram.types.Message._parse(
                    self.client,
                    update.message,
                    users,
                    chats,
                    business_connection_id=update.connection_id
                ),
                BotBusinessMessageHandler
            )

        async def edited_message_parser(update, users, chats):
            # Edited messages are parsed the same way as new messages, but the handler is different
            parsed, _ = await message_parser(update, users, chats)

            return (
                parsed,
                EditedMessageHandler
            )

        async def edited_bot_business_message_parser(update, users, chats):
            # Edited messages are parsed the same way as new messages, but the handler is different
            parsed, _ = await bot_business_message_parser(update, users, chats)

            return (
                parsed,
                EditedBotBusinessMessageHandler
            )

        async def deleted_messages_parser(update, users, chats):
            return (
                utils.parse_deleted_messages(self.client, update),
                DeletedMessagesHandler
            )

        async def deleted_bot_business_messages_parser(update, users, chats):
            return (
                utils.parse_deleted_messages(self.client, update, business_connection_id=update.connection_id),
                DeletedBotBusinessMessagesHandler
            )

        async def callback_query_parser(update, users, chats):
            return (
                await pyrogram.types.CallbackQuery._parse(self.client, update, users),
                CallbackQueryHandler
            )

        async def user_status_parser(update, users, chats):
            return (
                pyrogram.types.User._parse_user_status(self.client, update),
                UserStatusHandler
            )

        async def inline_query_parser(update, users, chats):
            return (
                pyrogram.types.InlineQuery._parse(self.client, update, users),
                InlineQueryHandler
            )

        async def poll_parser(update, users, chats):
            return (
                await pyrogram.types.Poll._parse_update(self.client, update, users),
                PollHandler
            )

        async def chosen_inline_result_parser(update, users, chats):
            return (
                pyrogram.types.ChosenInlineResult._parse(self.client, update, users),
                ChosenInlineResultHandler
            )

        async def chat_member_updated_parser(update, users, chats):
            return (
                pyrogram.types.ChatMemberUpdated._parse(self.client, update, users, chats),
                ChatMemberUpdatedHandler
            )

        async def chat_join_request_parser(update, users, chats):
            return (
                pyrogram.types.ChatJoinRequest._parse(self.client, update, users, chats),
                ChatJoinRequestHandler
            )

        async def story_parser(update, users, chats):
            return (
                await pyrogram.types.Story._parse(self.client, update.story, update.peer),
                StoryHandler
            )

        async def shipping_query_parser(update, users, chats):
            return (
                await pyrogram.types.ShippingQuery._parse(self.client, update, users),
                ShippingQueryHandler
            )

        async def pre_checkout_query_parser(update, users, chats):
            return (
                await pyrogram.types.PreCheckoutQuery._parse(self.client, update, users),
                PreCheckoutQueryHandler
            )

        async def message_bot_na_reaction_parser(update, users, chats):
            return (
                pyrogram.types.MessageReactionUpdated._parse(self.client, update, users, chats),
                MessageReactionUpdatedHandler
            )

        async def message_bot_a_reaction_parser(update, users, chats):
            return (
                pyrogram.types.MessageReactionCountUpdated._parse(self.client, update, users, chats),
                MessageReactionCountUpdatedHandler
            )

        async def bot_business_connect_parser(update, users, chats):
            return (
                await pyrogram.types.BotBusinessConnection._parse(self.client, update.connection),
                BotBusinessConnectHandler
            )

        async def purchased_paid_media_parser(update, users, chats):
            return (
                pyrogram.types.PurchasedPaidMedia._parse(self.client, update, users),
                PurchasedPaidMediaHandler
            )

        self.update_parsers = {
            Dispatcher.NEW_MESSAGE_UPDATES: message_parser,
            Dispatcher.NEW_BOT_BUSINESS_MESSAGE_UPDATES: bot_business_message_parser,
            Dispatcher.EDIT_MESSAGE_UPDATES: edited_message_parser,
            Dispatcher.EDIT_BOT_BUSINESS_MESSAGE_UPDATES: edited_bot_business_message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.DELETE_BOT_BUSINESS_MESSAGES_UPDATES: deleted_bot_business_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            Dispatcher.USER_STATUS_UPDATES: user_status_parser,
            Dispatcher.BOT_INLINE_QUERY_UPDATES: inline_query_parser,
            Dispatcher.POLL_UPDATES: poll_parser,
            Dispatcher.CHOSEN_INLINE_RESULT_UPDATES: chosen_inline_result_parser,
            Dispatcher.CHAT_MEMBER_UPDATES: chat_member_updated_parser,
            Dispatcher.CHAT_JOIN_REQUEST_UPDATES: chat_join_request_parser,
            Dispatcher.NEW_STORY_UPDATES: story_parser,
            Dispatcher.SHIPPING_QUERY_UPDATES: shipping_query_parser,
            Dispatcher.PRE_CHECKOUT_QUERY_UPDATES: pre_checkout_query_parser,
            Dispatcher.MESSAGE_BOT_NA_REACTION_UPDATES: message_bot_na_reaction_parser,
            Dispatcher.MESSAGE_BOT_A_REACTION_UPDATES: message_bot_a_reaction_parser,
            Dispatcher.BOT_BUSSINESS_CONNECT_UPDATES: bot_business_connect_parser,
            Dispatcher.PURCHASED_PAID_MEDIA_UPDATES: purchased_paid_media_parser
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}

    async def start(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(self.handler_worker(self.locks_list[-1]))
                )

            log.info("Started %s HandlerTasks", self.client.workers)

            if not self.client.skip_updates:
                await self.client.recover_gaps()

    async def stop(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()
            self.error_handlers.clear()

            log.info("Stopped %s HandlerTasks", self.client.workers)

    def add_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if isinstance(handler, ErrorHandler):
                    if handler not in self.error_handlers:
                        self.error_handlers.append(handler)
                else:
                    if group not in self.groups:
                        self.groups[group] = []
                        self.groups = OrderedDict(sorted(self.groups.items()))
                    self.groups[group].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    def remove_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if isinstance(handler, ErrorHandler):
                    if handler not in self.error_handlers:
                        raise ValueError(
                            f"Error handler {handler} does not exist. Handler was not removed."
                        )
                    self.error_handlers.remove(handler)
                else:
                    if group not in self.groups:
                        raise ValueError(f"Group {group} does not exist. Handler was not removed.")
                    self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    async def handler_worker(self, lock: asyncio.Lock):
        while True:
            packet = await self.updates_queue.get()
            if packet is None:
                break
            await self._process_packet(packet, lock)

    async def _process_packet(
        self,
        packet: tuple[raw.core.TLObject, dict[int, types.Update], dict[int, types.Update]],
        lock: asyncio.Lock,
    ):
        try:
            update, users, chats = packet
            parser = self.update_parsers.get(type(update))

            if parser is not None:
                parsed_result = parser(update, users, chats)
                if inspect.isawaitable(parsed_result):
                    parsed_update, handler_type = await parsed_result
                else:
                    parsed_update, handler_type = parsed_result
            else:
                parsed_update, handler_type = (None, type(None))

            async with lock:
                for group in self.groups.values():
                    for handler in group:
                        try:
                            if parsed_update is not None:
                                if isinstance(handler, handler_type) and await handler.check(
                                    self.client, parsed_update
                                ):
                                    await self._execute_callback(handler, parsed_update)
                                    break
                            elif isinstance(handler, RawUpdateHandler):
                                await self._execute_callback(handler, update, users, chats)
                                break
                        except (pyrogram.StopPropagation, pyrogram.ContinuePropagation) as e:
                            if isinstance(e, pyrogram.StopPropagation):
                                raise
                        except Exception as exception:
                            if parsed_update is not None:
                                await self._handle_exception(parsed_update, exception)
        except pyrogram.StopPropagation:
            pass
        except Exception as e:
            log.exception(e)
        finally:
            self.updates_queue.task_done()

    async def _handle_exception(self, parsed_update: types.Update, exception: Exception):
        handled_error = False
        for error_handler in self.error_handlers:
            try:
                if await error_handler.check(self.client, parsed_update, exception):
                    handled_error = True
                    break
            except pyrogram.StopPropagation:
                raise
            except pyrogram.ContinuePropagation:
                continue
            except Exception as inner_exception:
                log.exception("Error in error handler: %s", inner_exception)

        if not handled_error:
            log.exception("Unhandled exception: %s", exception)

    async def _execute_callback(self, handler: Handler, *args):
        if inspect.iscoroutinefunction(handler.callback):
            await handler.callback(self.client, *args)
        else:
            await self.client.loop.run_in_executor(
                self.client.executor, handler.callback, self.client, *args
            )