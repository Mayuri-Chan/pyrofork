#  Pyrofork - Telegram MTProto API Client Library for Python
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

from typing import Optional

from pyrogram import raw


def parse_button_style(style: Optional["raw.types.KeyboardButtonStyle"]) -> Optional[str]:
    """Parse KeyboardButtonStyle to string value."""
    if style is None:
        return None

    if getattr(style, "bg_primary", False):
        return "primary"

    if getattr(style, "bg_danger", False):
        return "danger"

    if getattr(style, "bg_success", False):
        return "success"

    return None


def write_button_style(style: Optional[str]) -> Optional["raw.types.KeyboardButtonStyle"]:
    """Convert string style to KeyboardButtonStyle."""
    if style is None:
        return None

    style_value = str(style).strip().lower()

    if style_value == "primary":
        return raw.types.KeyboardButtonStyle(bg_primary=True)

    if style_value == "danger":
        return raw.types.KeyboardButtonStyle(bg_danger=True)

    if style_value == "success":
        return raw.types.KeyboardButtonStyle(bg_success=True)

    raise ValueError(f"Unsupported button style: {style}")