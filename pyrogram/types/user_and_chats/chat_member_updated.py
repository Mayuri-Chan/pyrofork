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

from datetime import datetime
from typing import Dict, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from ..object import Object
from ..update import Update


class ChatMemberUpdated(Object, Update):
    """Represents changes in the status of a chat member.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Chat the user belongs to.

        from_user (:obj:`~pyrogram.types.User`):
            Performer of the action, which resulted in the change.

        date (:py:obj:`~datetime.datetime`):
            Date the change was done.

        old_chat_member (:obj:`~pyrogram.types.ChatMember`, *optional*):
            Previous information about the chat member.

        new_chat_member (:obj:`~pyrogram.types.ChatMember`, *optional*):
            New information about the chat member.

        invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Chat invite link, which was used by the user to join the chat; for joining by invite link events only.

        via_join_request (``bool``, *optional*):
            True, if the user joined the chat after sending a direct join request and being approved by an administrator

        via_chat_folder_invite_link (``bool``, *optional*):
            True, if the user joined the chat via a chat folder invite link
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        from_user: "types.User",
        date: datetime,
        old_chat_member: "types.ChatMember",
        new_chat_member: "types.ChatMember",
        invite_link: "types.ChatInviteLink" = None,
        via_join_request: bool = None,
        via_chat_folder_invite_link: bool = False,
        _raw: "raw.base.Update" = None
    ):
        super().__init__(client)

        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.old_chat_member = old_chat_member
        self.new_chat_member = new_chat_member
        self.invite_link = invite_link
        self.via_join_request = via_join_request
        self.via_chat_folder_invite_link = via_chat_folder_invite_link
        self.raw = _raw

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: Union["raw.types.UpdateChatParticipant", "raw.types.UpdateChannelParticipant", "raw.types.UpdateBotStopped"],
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "ChatMemberUpdated":
        if isinstance(update, raw.types.UpdateBotStopped):
            from_user = types.User._parse(client, users[update.user_id])
            _chat_member_one = types.ChatMember(
                user=from_user,
                status=enums.ChatMemberStatus.BANNED,
                client=client
            )
            _chat_member_two = types.ChatMember(
                user=from_user,
                status=enums.ChatMemberStatus.MEMBER,
                client=client
            )
            if update.stopped:
                return ChatMemberUpdated(
                    chat=types.Chat._parse_chat(client, users[update.user_id]),
                    from_user=from_user,
                    date=utils.timestamp_to_datetime(update.date),
                    old_chat_member=_chat_member_two,
                    new_chat_member=_chat_member_one,
                    client=client
                )
            return ChatMemberUpdated(
                chat=types.Chat._parse_chat(client, users[update.user_id]),
                from_user=from_user,
                date=utils.timestamp_to_datetime(update.date),
                old_chat_member=_chat_member_one,
                new_chat_member=_chat_member_two,
                client=client
            )

        chat_id = getattr(update, "chat_id", None) or getattr(update, "channel_id")

        old_chat_member = None
        new_chat_member = None
        invite_link = None
        via_join_request = None

        if update.prev_participant:
            old_chat_member = types.ChatMember._parse(client, update.prev_participant, users, chats)

        if update.new_participant:
            new_chat_member = types.ChatMember._parse(client, update.new_participant, users, chats)

        if update.invite:
            invite_link = types.ChatInviteLink._parse(client, update.invite, users)
            if isinstance(update.invite, raw.types.ChatInvitePublicJoinRequests):
                via_join_request = True

        return ChatMemberUpdated(
            chat=types.Chat._parse_chat(client, chats[chat_id]),
            from_user=types.User._parse(client, users[update.actor_id]),
            date=utils.timestamp_to_datetime(update.date),
            old_chat_member=old_chat_member,
            new_chat_member=new_chat_member,
            invite_link=invite_link,
            via_join_request=via_join_request,
            via_chat_folder_invite_link=getattr(update, "via_chatlist", False),
            _raw=update,
            client=client
        )
