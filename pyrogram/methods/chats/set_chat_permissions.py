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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class SetChatPermissions:
    async def set_chat_permissions(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        permissions: "types.ChatPermissions",
    ) -> "types.Chat":
        """Set default chat permissions for all members.

        You must be an administrator in the group or a supergroup for this to work and must have the
        *can_restrict_members* admin rights.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            permissions (:obj:`~pyrogram.types.ChatPermissions`):
                New default chat permissions.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import ChatPermissions

                # Completely restrict chat
                await app.set_chat_permissions(chat_id, ChatPermissions())

                # Chat members can only send text messages and media messages
                await app.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True
                    )
                )
        """

        r = await self.invoke(
            raw.functions.messages.EditChatDefaultBannedRights(
                peer=await self.resolve_peer(chat_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=0,
                    send_messages=not permissions.can_send_messages if permissions.can_send_messages is not None else None,
                    send_media=not permissions.can_send_media_messages if permissions.can_send_media_messages is not None else None,
                    embed_links=not permissions.can_add_web_page_previews if permissions.can_add_web_page_previews is not None else None,
                    send_polls=not permissions.can_send_polls if permissions.can_send_polls is not None else None,
                    change_info=not permissions.can_change_info if permissions.can_change_info is not None else None,
                    invite_users=not permissions.can_invite_users if permissions.can_invite_users is not None else None,
                    pin_messages=not permissions.can_pin_messages if permissions.can_pin_messages is not None else None,
                    manage_topics=not permissions.can_manage_topics if permissions.can_manage_topics is not None else None,
                    send_audios=not permissions.can_send_audios if permissions.can_send_audios is not None else None,
                    send_docs=not permissions.can_send_docs if permissions.can_send_docs is not None else None,
                    send_games=not permissions.can_send_games if permissions.can_send_games is not None else None,
                    send_gifs=not permissions.can_send_gifs if permissions.can_send_gifs is not None else None,
                    send_inline=not permissions.can_send_inline if permissions.can_send_inline is not None else None,
                    send_photos=not permissions.can_send_photos if permissions.can_send_photos is not None else None,
                    send_plain=not permissions.can_send_plain if permissions.can_send_plain is not None else None,
                    send_roundvideos=not permissions.can_send_roundvideos if permissions.can_send_roundvideos is not None else None,
                    send_stickers=not permissions.can_send_stickers if permissions.can_send_stickers is not None else None,
                    send_videos=not permissions.can_send_videos if permissions.can_send_videos is not None else None,
                    send_voices=not permissions.can_send_voices if permissions.can_send_voices is not None else None
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
