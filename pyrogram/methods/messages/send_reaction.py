#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, List

import pyrogram
from pyrogram import raw, types


class SendReaction:
    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        emoji: Union[int, str, List[Union[int, str]]] = None,
        big: bool = False,
        add_to_recent: bool = False
    ) -> "types.MessageReactions":
        """Use this method to send reactions on a message/stories.
        Service messages can't be reacted to.
        Automatically forwarded messages from
        a channel to its discussion group have the
        same available reactions as messages in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``, *optional*):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            story_id (``int``, *optional*):
                Identifier of the story.

            emoji (``int`` | ``str`` | List of ``int`` | ``str``, *optional*):
                Reaction emoji.
                Pass None as emoji (default) to retract the reaction.
                Pass list of int or str to react multiple emojis.

            big (``bool``, *optional*):
                Pass True to set the reaction with a big animation.
                For message reactions only.
                Defaults to False.
                
            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.

        Returns:
            :obj:`~pyrogram.types.MessageReactions`: On success, True is returned.

        Example:
            .. code-block:: python

                # Send a reaction
                await app.send_reaction(chat_id, message_id=message_id, emoji="🔥")
                await app.send_reaction(chat_id, story_id=story_id, emoji="🔥")

                # Send a multiple reactions
                await app.send_reaction(chat_id, message_id=message_id, emoji=["🔥", "❤️"])

                # Retract a reaction
                await app.send_reaction(chat_id, message_id=message_id)
                await app.send_reaction(chat_id, story_id=story_id)
        """
        if isinstance(emoji, list):
            reaction = [
                    raw.types.ReactionCustomEmoji(document_id=i)
                    if isinstance(i, int)
                    else raw.types.ReactionEmoji(emoticon=i)
                    for i in emoji
            ] if emoji else None
        else:
            if isinstance(emoji, int):
                reaction = [raw.types.ReactionCustomEmoji(document_id=emoji)]
            else:
                reaction = [raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None
        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=reaction,
                    big=big,
                    add_to_recent=add_to_recent
                )
            )
            for i in r.updates:
              if isinstance(i, raw.types.UpdateMessageReactions):
                  return types.MessageReactions._parse(self, i.reactions)
        elif story_id is not None:
            await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=raw.types.ReactionEmoji(emoticon=emoji) if emoji else None,
                    add_to_recent=add_to_recent
                )
            )
            return True
        else:
            raise ValueError("You need to pass one of message_id!")
