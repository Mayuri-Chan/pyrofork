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

import pyrofork
from pyrofork import raw, types
from .menu_button import MenuButton


class MenuButtonWebApp(MenuButton):
    """A menu button, which launches a `Web App <https://core.telegram.org/bots/webapps>`_.

    Parameters:
        text (``str``):
            Text on the button

        web_app (:obj:`~pyrofork.types.WebAppInfo`):
            Description of the Web App that will be launched when the user presses the button.
            The Web App will be able to send an arbitrary message on behalf of the user using the method
            :meth:`~pyrofork.Client.answer_web_app_query`.
    """

    def __init__(
        self,
        text: str,
        web_app: "types.WebAppInfo"
    ):
        super().__init__("web_app")

        self.text = text
        self.web_app = web_app

    async def write(self, client: "pyrofork.Client") -> "raw.types.BotMenuButton":
        return raw.types.BotMenuButton(
            text=self.text,
            url=self.web_app.url
        )
