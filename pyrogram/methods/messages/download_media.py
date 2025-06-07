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
import os
from datetime import datetime
from typing import Union, Optional, Callable, BinaryIO

import pyrogram
from pyrogram import types
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES

DEFAULT_DOWNLOAD_DIR = "downloads/"


class DownloadMedia:
    async def download_media(
        self: "pyrogram.Client",
        message: Union["types.Message", "types.Story", str],
        file_name: str = DEFAULT_DOWNLOAD_DIR,
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional[Union[str, BinaryIO]]:
        """Download the media from a message.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            message (:obj:`~pyrogram.types.Message` | :obj:`~pyrogram.types.Story` | ``str``):
                Pass a Message/Story containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            in_memory (``bool``, *optional*):
                Pass True to download the media in-memory.
                A binary file-like object with its attribute ".name" set will be returned.
                Defaults to False.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``str`` | ``None`` | ``BinaryIO``: On success, the absolute path of the downloaded file is returned,
            otherwise, in case the download failed or was deliberately stopped with
            :meth:`~pyrogram.Client.stop_transmission`, None is returned.
            Otherwise, in case ``in_memory=True``, a binary file-like object with its attribute ".name" set is returned.

        Raises:
            ValueError: if the message doesn't contain any downloadable media

        Example:
            Download media to file

            .. code-block:: python

                # Download from Message
                await app.download_media(message)

                # Download from file id
                await app.download_media(message.photo.file_id)

                # Keep track of the progress while downloading
                async def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                await app.download_media(message, progress=progress)

            Download media in-memory

            .. code-block:: python

                file = await app.download_media(message, in_memory=True)

                file_name = file.name
                file_bytes = bytes(file.getbuffer())
        """
        available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note",
                           "new_chat_photo")

        if isinstance(message, types.Message) or isinstance(message, types.Story):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                raise ValueError("This message doesn't contain any downloadable media")
        else:
            media = message

        if isinstance(media, str):
            file_id_str = media
        else:
            file_id_str = media.file_id

        file_id_obj = FileId.decode(file_id_str)

        file_type = file_id_obj.file_type
        media_file_name = getattr(media, "file_name", "")
        file_size = getattr(media, "file_size", 0)
        mime_type = getattr(media, "mime_type", "")
        date = getattr(media, "date", None)

        directory, file_name = os.path.split(file_name)
        file_name = file_name or media_file_name or ""

        if not os.path.isabs(file_name):
            directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

        if not file_name:
            guessed_extension = self.guess_extension(mime_type)

            if file_type in PHOTO_TYPES:
                extension = ".jpg"
            elif file_type == FileType.VOICE:
                extension = guessed_extension or ".ogg"
            elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
                extension = guessed_extension or ".mp4"
            elif file_type == FileType.DOCUMENT:
                extension = guessed_extension or ".zip"
            elif file_type == FileType.STICKER:
                extension = guessed_extension or ".webp"
            elif file_type == FileType.AUDIO:
                extension = guessed_extension or ".mp3"
            else:
                extension = ".unknown"

            file_name = "{}_{}_{}{}".format(
                FileType(file_id_obj.file_type).name.lower(),
                (date or datetime.now()).strftime("%Y-%m-%d_%H-%M-%S"),
                self.rnd_id(),
                extension
            )

        downloader = self.handle_download(
            (file_id_obj, directory, file_name, in_memory, file_size, progress, progress_args)
        )

        if block:
            return await downloader
        else:
            self.loop.create_task(downloader)
