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

from typing import Union, BinaryIO, List

import pyrogram
from pyrogram import raw


class SetProfilePhoto:
    async def set_profile_photo(
        self: "pyrogram.Client",
        *,
        photo: Union[str, BinaryIO] = None,
        emoji: int = None,
        emoji_background: Union[int, List[int]] = None,
        video: Union[str, BinaryIO] = None
    ) -> bool:
        """Set a new profile photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see examples below).

        .. note::

            This bots method only works for photo only.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            emoji (``int``, *optional*):
                Unique identifier (int) of the emoji to be used as the profile photo.

            emoji_background (``int`` | ``List[int]``, *optional*):
                hexadecimal colors or List of hexadecimal colors to be used as the chat photo background.

            video (``str`` | ``BinaryIO``, *optional*):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set a new profile photo
                await app.set_profile_photo(photo="new_photo.jpg")

                # Set a new profile video
                await app.set_profile_photo(video="new_video.mp4")
        """

        emoji_id = None
        if emoji:
            background_colors = emoji_background if emoji_background is not None else [0xFFFFFF]
            if isinstance(background_colors, int):
                background_colors = [background_colors]
            emoji_id = raw.types.VideoSizeEmojiMarkup(
                emoji_id=emoji,
                background_colors=background_colors
            )

        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    file=await self.save_file(photo),
                    video_emoji_markup=emoji_id,
                    video=await self.save_file(video)
                )
            )
        )
