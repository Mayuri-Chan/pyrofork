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

from typing import Optional, List, BinaryIO, Union

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaAudio(InputMedia):
    """An audio to be sent inside an album.

    It is intended to be used with :meth:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str`` | ``BinaryIO``):
            Audio to send.
            Pass a file_id as string to send an audio that exists on the Telegram servers or
            pass a file path as string to upload a new audio that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get an audio file from the Internet.

        thumb (``str``, *optional*):
            Thumbnail of the music file album cover.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        duration (``int``, *optional*):
            Duration of the audio in seconds

        performer (``str``, *optional*):
            Performer of the audio

        title (``str``, *optional*):
            Title of the audio

        file_name (``str``, *optional*):
            File name of the audio sent.
            Defaults to file's path basename.
    """

    def __init__(
        self,
        media: Union[str, BinaryIO],
        thumb: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List[MessageEntity] = None,
        duration: int = 0,
        performer: str = "",
        title: str = "",
        file_name: str = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title
        self.file_name = file_name
