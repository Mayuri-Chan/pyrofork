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

from typing import List, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils


class TranslateText:
    async def translate_message_text(
        self: "pyrogram.Client",
        to_language_code: str,
        chat_id: Optional[Union[int, str]] = None,
        message_ids: Optional[Union[int, List[int]]] = None,
        text: Optional[str] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None
    ) -> Union["types.TranslatedText", List["types.TranslatedText"]]:
        """Translates a text or message(s) to the given language. If the current user is a Telegram Premium user, then text formatting is preserved.

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message/text is translated.
                Must be one of the supported language codes.

            chat_id (``Optional[int | str]``):
                Unique identifier (int) or username (str) of the target chat.

            message_ids (``Optional[int | List[int]]``):
                Identifier or list of message identifiers of the target message(s).

            text (``Optional[str]``):
                Text to translate.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        Example:
            .. code-block:: python

                # Using chat_id and message_ids
                await app.translate_message_text("en", chat_id, message_ids)

                # Using text
                await app.translate_message_text("en", text="Hello, how are you?")

                # Using text with parse_mode
                await app.translate_message_text("en", text="*Hello*, how are you?", parse_mode=ParseMode.MARKDOWN)

                # Using text with entities
                entities = [types.MessageEntityBold(offset=0, length=5)]
                await app.translate_message_text("en", text="*Hello*, how are you?", entities=entities)

        Returns:
            :obj:`~pyrogram.types.TranslatedText` | List of :obj:`~pyrogram.types.TranslatedText`: In case *message_ids* was not
            a list, a single result is returned, otherwise a list of results is returned.
        """
        if text is not None:
            message, entities = (
                await utils.parse_text_entities(
                    self,
                    text,
                    parse_mode,
                    entities
                )
            ).values()

            r = await self.invoke(
                raw.functions.messages.TranslateText(
                    to_lang=to_language_code,
                    text=[
                        raw.types.TextWithEntities(
                            text=message,
                            entities=entities or []
                        )
                    ]
                )
            )

        elif chat_id is not None and message_ids is not None:
            ids = [message_ids] if not isinstance(message_ids, list) else message_ids

            r = await self.invoke(
                raw.functions.messages.TranslateText(
                    to_lang=to_language_code,
                    peer=await self.resolve_peer(chat_id),
                    id=ids
                )
            )
        else:
            raise ValueError("Either 'text' or both 'chat_id' and 'message_ids' must be provided.")

        return (
            types.TranslatedText._parse(self, r.result[0])
            if len(r.result) == 1
            else [
                types.TranslatedText._parse(self, i)
                for i in r.result
            ]
        )