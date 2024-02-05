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

from typing import List, Optional

import pyrofork
from pyrofork import raw, types, utils, enums
from .inline_query_result import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):
    """Link to an audio file.
    
    By default, this audio file will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    audio.
    
    Parameters:
        audio_url (``str``):
            A valid URL for the audio file.
            
        title (``str``):
            Title for the result.
            
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
            
        performer (``str``, *optional*):
            Audio performer.
            
        audio_duration (``int``, *optional*):
            Audio duration in seconds.

        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters.
            
        parse_mode (:obj:`~pyrofork.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrofork.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        description (``str``, *optional*):
            Short description of the result.
            
        reply_markup (:obj:`~pyrofork.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~pyrofork.types.InputMessageContent`, *optional*):
            Content of the message to be sent instead of the audio.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.
    """

    def __init__(
        self,
        audio_url: str,
        title: str,
        id: str = None,
        performer: str = "",
        audio_duration: int = 0,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        description: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_url = audio_url
        self.title = title
        self.performer = performer
        self.audio_duration = audio_duration
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.description = description
        self.thumb_url = thumb_url

    async def write(self, client: "pyrofork.Client"):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type="audio/mpeg",
            attributes=[raw.types.DocumentAttributeAudio(
                duration=self.audio_duration,
                title=self.title,
                performer=self.performer
            )]
        )

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            content=audio,
            description=self.description,
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            ) if self.thumb_url else None,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )
